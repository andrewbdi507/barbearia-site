#!/bin/bash
# ============================================================
# Barbershop SaaS — Media Backup Script
# ============================================================
# Usage:
#   bash scripts/backup-uploads.sh
#
# Backs up uploaded media files to S3/R2.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)

source "${PROJECT_DIR}/config/environments/.env.production" 2>/dev/null || true

UPLOAD_DIR="${UPLOAD_DIR:-${PROJECT_DIR}/storage/uploads}"
BACKUP_DIR="${PROJECT_DIR}/backups/uploads"

mkdir -p "${BACKUP_DIR}"

echo "============================================"
echo "  Barbershop SaaS — Uploads Backup"
echo "  Time: $(date)"
echo "============================================"

# ---- Tar and compress ----
BACKUP_FILE="${BACKUP_DIR}/uploads_${TIMESTAMP}.tar.gz"
echo "Compressing uploads..."
tar -czf "${BACKUP_FILE}" -C "$(dirname "${UPLOAD_DIR}")" "$(basename "${UPLOAD_DIR}")"

SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
echo "  Size: ${SIZE}"

# ---- Sync to remote ----
if command -v aws &> /dev/null && [ -n "${BACKUP_S3_BUCKET:-}" ]; then
    echo "Syncing to S3..."
    aws s3 cp "${BACKUP_FILE}" "s3://${BACKUP_S3_BUCKET}/uploads/" --storage-class STANDARD_IA
fi

if command -v rclone &> /dev/null && [ -n "${BACKUP_R2_REMOTE:-}" ]; then
    echo "Syncing to R2..."
    rclone copy "${BACKUP_FILE}" "${BACKUP_R2_REMOTE}/uploads/"
fi

# ---- Cleanup old (keep 7 days) ----
find "${BACKUP_DIR}" -name "*.tar.gz" -mtime +7 -delete

echo "✅ Uploads backup complete"
