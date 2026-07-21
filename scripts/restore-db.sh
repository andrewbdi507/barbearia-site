#!/bin/bash
# ============================================================
# Barbershop SaaS — Database Restore Script
# ============================================================
# Usage:
#   bash scripts/restore-db.sh <backup-file.dump.gz>
#
# WARNING: This overwrites the target database.
# Always restore on a separate instance first to verify.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if [ $# -lt 1 ]; then
    echo "Usage: bash scripts/restore-db.sh <backup-file.dump.gz>"
    echo ""
    echo "Available backups:"
    find "${PROJECT_DIR}/backups/postgres" -name "*.dump.gz" -type f | sort -r | head -20
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "❌ Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

# ---- Load environment ----
source "${PROJECT_DIR}/config/environments/.env.production" 2>/dev/null || true
DB_USER="${DB_USER:-barbershop}"
DB_NAME="${DB_NAME:-barbershop_production}"
DB_CONTAINER="${DB_CONTAINER:-barbershop-prod-postgres}"

echo "============================================"
echo "  Barbershop SaaS — Database Restore"
echo "  Time:    $(date)"
echo "  Source:  ${BACKUP_FILE}"
echo "  Target:  ${DB_NAME}"
echo "============================================"
echo ""
echo "⚠️  WARNING: This will OVERWRITE the database '${DB_NAME}'"
echo ""

# ---- Confirm ----
read -rp "Type 'RESTORE' to continue: " CONFIRM
if [ "${CONFIRM}" != "RESTORE" ]; then
    echo "❌ Restore cancelled."
    exit 0
fi

# ---- Stop dependent services ----
echo "[1/4] Stopping dependent services..."
docker compose -f "${PROJECT_DIR}/docker-compose.prod.yml" stop backend worker scheduler

# ---- Terminate active connections ----
echo "[2/4] Terminating active connections..."
docker exec "${DB_CONTAINER}" psql -U "${DB_USER}" -d postgres -c "
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = '${DB_NAME}'
    AND pid <> pg_backend_pid();
" 2>/dev/null || true

# ---- Drop & Recreate ----
echo "[3/4] Dropping and recreating database..."
docker exec "${DB_CONTAINER}" dropdb -U "${DB_USER}" --if-exists "${DB_NAME}"
docker exec "${DB_CONTAINER}" createdb -U "${DB_USER}" -O "${DB_USER}" "${DB_NAME}"

# ---- Restore ----
echo "[4/4] Restoring backup..."
gunzip -c "${BACKUP_FILE}" | docker exec -i "${DB_CONTAINER}" \
    pg_restore -U "${DB_USER}" -d "${DB_NAME}" --no-owner --no-acl --verbose

echo ""

# ---- Verify ----
echo "Verifying restore..."
TABLE_COUNT=$(docker exec "${DB_CONTAINER}" psql -U "${DB_USER}" -d "${DB_NAME}" -t -c "
    SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';
" | tr -d ' ')
echo "  Tables restored: ${TABLE_COUNT}"

# ---- Restart services ----
echo "Restarting services..."
docker compose -f "${PROJECT_DIR}/docker-compose.prod.yml" start backend worker scheduler

echo ""
echo "✅ Restore complete!"
echo "============================================"
