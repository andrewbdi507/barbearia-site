#!/bin/sh
# ============================================================
# AGENDA OS — Startup Script (Render Production)
# ============================================================
set -e

echo "============================================"
echo "  AGENDA OS — STARTUP"
echo "  $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "============================================"

export PYTHONPATH=/app

# ---- 1. DIAGNOSTIC ----
echo ""
echo "[1/4] DIAGNOSTIC"
echo "  DATABASE_URL present: $(if [ -n \"$DATABASE_URL\" ]; then echo 'YES'; else echo 'NO'; fi)"
echo "  PORT: ${PORT:-8000}"
echo "  Files: $(ls /app | tr '\n' ' ')"
echo "  alembic dir: $(if [ -d /app/alembic ]; then echo 'EXISTS'; else echo 'MISSING'; fi)"

# ---- 2. CREATE TABLES ----
echo ""
echo "[2/4] CREATING DATABASE TABLES"
python3 << 'PYEOF'
import os, sys, importlib

db_url = os.environ.get("DATABASE_URL", "")
if not db_url:
    print("  FATAL: DATABASE_URL not set")
    sys.exit(1)

from urllib.parse import urlparse
p = urlparse(db_url)
print(f"  Host: {p.hostname}:{p.port or 5432}/{p.path.lstrip('/')}")

sync_url = db_url.replace("+asyncpg", "+psycopg2")
if "+psycopg2" not in sync_url:
    sync_url = sync_url.replace("postgresql://", "postgresql+psycopg2://")

from sqlalchemy import create_engine, inspect
from app.infrastructure.database.base import Base

model_modules = [
    "app.modules.auth.infrastructure.models.auth_models",
    "app.modules.tenant.infrastructure.models.tenant_models",
    "app.modules.staff.infrastructure.models.staff_models",
    "app.modules.customer.infrastructure.models.customer_models",
    "app.modules.scheduling.infrastructure.models.scheduling_models",
    "app.modules.payment.infrastructure.models.payment_models",
    "app.modules.notification.infrastructure.models.notification_models",
    "app.modules.analytics.infrastructure.models.analytics_models",
    "app.modules.site.infrastructure.models.site_models",
]
for mod in model_modules:
    try:
        importlib.import_module(mod)
    except Exception as e:
        print(f"  Warning: skip {mod}: {e}")

engine = create_engine(sync_url)
inspector = inspect(engine)
before = len(inspector.get_table_names())
Base.metadata.create_all(engine)
after = len(inspector.get_table_names())
print(f"  Tables: {before} -> {after} (created {after - before})")
engine.dispose()
PYEOF

# ---- 3. ALEMBIC STAMP ----
echo ""
echo "[3/4] ALEMBIC STAMP"
PYTHONPATH=/app alembic -c /app/alembic/alembic.ini stamp head 2>/dev/null && \
  echo "  Alembic stamped OK" || \
  echo "  Alembic skipped (no migrations yet)"

# ---- 4. START SERVER ----
echo ""
echo "[4/4] STARTING SERVER on :${PORT:-8000}"
exec uvicorn app.presentation.api.app:create_app --factory --host 0.0.0.0 --port "${PORT:-8000}"
