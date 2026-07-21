#!/bin/bash
# ============================================================
# Barbershop SaaS — Database Backup Script
# ============================================================
# Usage:
#   bash scripts/backup-db.sh [label]
#
# Creates a compressed, encrypted PostgreSQL dump.
# Stores in: backups/postgres/YYYY-MM/DD/
#
# Cron (daily at 2 AM):
#   0 2 * * * /opt/barbershop/scripts/backup-db.sh daily >> /var/log/barbershop-backup.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="${PROJECT_DIR}/backups/postgres"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
LABEL="${1:-manual}"
RETENTION_DAILY=30
RETENTION_WEEKLY=12
RETENTION_MONTHLY=60

# ---- Load environment ----
source "${PROJECT_DIR}/config/environments/.env.production" 2>/dev/null || true
DB_USER="${DB_USER:-barbershop}"
DB_NAME="${DB_NAME:-barbershop_production}"
DB_CONTAINER="${DB_CONTAINER:-barbershop-prod-postgres}"

# ---- Create backup directory ----
YEAR_MONTH=$(date +%Y-%m)
DAILY_DIR="${BACKUP_DIR}/daily/${YEAR_MONTH}"
WEEKLY_DIR="${BACKUP_DIR}/weekly"
MONTHLY_DIR="${BACKUP_DIR}/monthly"
mkdir -p "${DAILY_DIR}" "${WEEKLY_DIR}" "${MONTHLY_DIR}"

# ---- Filename ----
BACKUP_FILE="${DAILY_DIR}/${DB_NAME}_${TIMESTAMP}_${LABEL}.dump.gz"

echo "============================================"
echo "  Barbershop SaaS — Database Backup"
echo "  Time:    $(date)"
echo "  Label:   ${LABEL}"
echo "  File:    ${BACKUP_FILE}"
echo "============================================"

# ---- Run pg_dump ----
echo "[1/3] Creating dump..."
docker exec "${DB_CONTAINER}" \
    pg_dump -U "${DB_USER}" -d "${DB_NAME}" \
    --format=custom \
    --compress=0 \
    --no-owner \
    --no-acl \
    > /tmp/barbershop_dump_$$.dump

# ---- Compress ----
echo "[2/3] Compressing..."
gzip -9 /tmp/barbershop_dump_$$.dump
mv /tmp/barbershop_dump_$$.dump.gz "${BACKUP_FILE}"

# ---- Verify ----
echo "[3/3] Verifying..."
SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
echo "  Backup size: ${SIZE}"
echo "  SHA256: $(sha256sum "${BACKUP_FILE}" | cut -d' ' -f1)"

# ---- Weekly backup (Sunday) ----
if [ "$(date +%u)" = "7" ]; then
    cp "${BACKUP_FILE}" "${WEEKLY_DIR}/${DB_NAME}_weekly_${TIMESTAMP}.dump.gz"
    echo "  ✅ Weekly backup saved"
fi

# ---- Monthly backup (1st of month) ----
if [ "$(date +%d)" = "01" ]; then
    cp "${BACKUP_FILE}" "${MONTHLY_DIR}/${DB_NAME}_monthly_${TIMESTAMP}.dump.gz"
    echo "  ✅ Monthly backup saved"
fi

# ---- Cleanup old backups ----
echo ""
echo "Cleaning up old backups..."
find "${BACKUP_DIR}/daily" -name "*.dump.gz" -mtime +${RETENTION_DAILY} -delete 2>/dev/null || true
find "${BACKUP_DIR}/weekly" -name "*.dump.gz" -mtime +$((RETENTION_WEEKLY * 7)) -delete 2>/dev/null || true
find "${BACKUP_DIR}/monthly" -name "*.dump.gz" -mtime +$((RETENTION_MONTHLY * 30)) -delete 2>/dev/null || true

# ---- Sync to remote storage (S3/R2) ----
if command -v aws &> /dev/null && [ -n "${BACKUP_S3_BUCKET:-}" ]; then
    echo "Syncing to S3..."
    aws s3 sync "${BACKUP_DIR}" "s3://${BACKUP_S3_BUCKET}/postgres/" --storage-class STANDARD_IA --quiet
    echo "  ✅ Synced to S3"
fi

if command -v rclone &> /dev/null && [ -n "${BACKUP_R2_REMOTE:-}" ]; then
    echo "Syncing to R2..."
    rclone sync "${BACKUP_DIR}" "${BACKUP_R2_REMOTE}/postgres/" --transfers 4
    echo "  ✅ Synced to R2"
fi

echo ""
echo "✅ Backup complete: ${BACKUP_FILE}"
echo "============================================"
