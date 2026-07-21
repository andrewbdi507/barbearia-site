#!/bin/bash
# ============================================================
# AGENDA OS — Backup Script
# ============================================================
# Daily backup of PostgreSQL database with S3/R2 upload.
#
# Usage:
#   chmod +x backup.sh
#   ./backup.sh                    # Manual backup
#   0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1  # Cron daily 2am
#
# Environment:
#   DB_USER, DB_PASSWORD, DB_NAME  — PostgreSQL credentials
#   BACKUP_RETENTION_DAYS          — Days to keep (default 30)
#   R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME, R2_ENDPOINT  — R2 upload
# ============================================================

set -euo pipefail

# ---- Configuration ----
BACKUP_DIR="${BACKUP_DIR:-/opt/backups}"
DB_USER="${DB_USER:-agendaos}"
DB_PASSWORD="${DB_PASSWORD}"
DB_NAME="${DB_NAME:-agendaos_prod}"
DB_HOST="${DB_HOST:-postgres}"
DB_PORT="${DB_PORT:-5432}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/agendaos_${DATE}.sql.gz"

# ---- Ensure backup dir ----
mkdir -p "$BACKUP_DIR"

# ---- Dump & Compress ----
echo "[$(date)] Starting backup: $DB_NAME"

PGPASSWORD="$DB_PASSWORD" pg_dump \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  --no-owner --no-acl \
  | gzip > "$BACKUP_FILE"

SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "[$(date)] Backup completed: $BACKUP_FILE ($SIZE)"

# ---- Upload to S3/R2 (if configured) ----
if [ -n "${R2_ACCESS_KEY_ID:-}" ] && [ -n "${R2_BUCKET_NAME:-}" ]; then
  echo "[$(date)] Uploading to R2..."
  AWS_ACCESS_KEY_ID="$R2_ACCESS_KEY_ID" \
  AWS_SECRET_ACCESS_KEY="$R2_SECRET_ACCESS_KEY" \
  AWS_DEFAULT_REGION=auto \
  aws s3 cp "$BACKUP_FILE" "s3://${R2_BUCKET_NAME}/backups/agendaos_${DATE}.sql.gz" \
    --endpoint-url "$R2_ENDPOINT" \
    --quiet && echo "[$(date)] Upload OK" || echo "[$(date)] Upload FAILED"
fi

# ---- Cleanup old backups ----
echo "[$(date)] Cleaning backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "*.sql.gz" -mtime "+$RETENTION_DAYS" -delete
echo "[$(date)] Cleanup completed. Backups remaining: $(find "$BACKUP_DIR" -name "*.sql.gz" | wc -l)"

# ---- Verify latest backup ----
LATEST=$(find "$BACKUP_DIR" -name "*.sql.gz" -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)
if [ -n "$LATEST" ]; then
  echo "[$(date)] Latest backup: $LATEST"
  # Quick integrity check
  gzip -t "$LATEST" && echo "[$(date)] Integrity check: OK" || echo "[$(date)] Integrity check: FAILED"
fi

echo "[$(date)] Backup job completed successfully"
