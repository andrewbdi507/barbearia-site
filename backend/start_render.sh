#!/bin/bash
# ============================================================
# AGENDA OS — Startup Script (Render Python Native)
# ============================================================
set -e

echo "============================================"
echo "  AGENDA OS — STARTUP (Python Native)"
echo "  $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "============================================"

# ---- 1. Run Alembic migrations ----
echo ""
echo "[1/2] Running database migrations..."
cd /opt/render/project/src/backend 2>/dev/null || cd /opt/render/project/src
alembic upgrade head
echo "  Migrations OK"

# ---- 2. Start server ----
echo ""
echo "[2/2] Starting server on :${PORT:-10000}"
exec uvicorn app.presentation.api.app:create_app --factory --host 0.0.0.0 --port "${PORT:-10000}"
