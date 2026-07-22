#!/usr/bin/env bash
# ============================================================
# AGENDA OS — Startup Script (Render Python Native)
# rootDir = backend, so CWD is already backend/
# ============================================================
set -e

echo "============================================"
echo "  AGENDA OS — STARTUP"
echo "  $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "============================================"

# ---- 1. Run Alembic migrations ----
echo ""
echo "[1/2] Running database migrations..."
alembic -c alembic/alembic.ini upgrade head
echo "  Migrations OK"

# ---- 2. Start server ----
echo ""
echo "[2/2] Starting server on :${PORT:-10000}"
exec uvicorn app.presentation.api.app:create_app --factory --host 0.0.0.0 --port "${PORT:-10000}"
