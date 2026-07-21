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

# ---- 1. CREATE TABLES ----
echo ""
echo "[1/3] CREATING DATABASE TABLES"

cat > /tmp/create_tables.py << 'PYEOF'
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
# Render requires SSL
if "render.com" in sync_url and "sslmode" not in sync_url:
    sync_url += "?sslmode=require"

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

# Seed default plans if not exist
from sqlalchemy import text
with engine.connect() as conn:
    existing = conn.execute(text("SELECT COUNT(*) FROM plans")).scalar()
    if existing == 0:
        conn.execute(text("""
            INSERT INTO plans (id, slug, name, price_cents, max_bookings, max_staff, is_active, created_at, updated_at)
            VALUES 
            (gen_random_uuid(), 'starter', 'Starter', 4900, 100, 1, true, now(), now()),
            (gen_random_uuid(), 'pro', 'Pro', 9900, 999999, 5, true, now(), now()),
            (gen_random_uuid(), 'premium', 'Premium', 19900, 999999, 999999, true, now(), now())
        """))
        conn.commit()
        print("  Default plans seeded")
    else:
        print(f"  Plans already exist: {existing}")

engine.dispose()
PYEOF

DATABASE_URL="$DATABASE_URL" python3 /tmp/create_tables.py

# ---- 2. ALEMBIC STAMP ----
echo ""
echo "[2/3] ALEMBIC STAMP"
PYTHONPATH=/app alembic -c /app/alembic/alembic.ini stamp head 2>/dev/null && \
  echo "  Alembic stamped OK" || \
  echo "  Alembic skipped (no migrations yet)"

# ---- 3. START SERVER ----
echo ""
echo "[3/3] STARTING SERVER on :${PORT:-8000}"
exec uvicorn app.presentation.api.app:create_app --factory --host 0.0.0.0 --port "${PORT:-8000}"
exec uvicorn app.presentation.api.app:create_app --factory --host 0.0.0.0 --port "${PORT:-8000}"
