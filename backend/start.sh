#!/bin/sh
# ============================================================
# AGENDA OS — Startup Script (Render Production)
# ============================================================

set -e
export PYTHONPATH=/app

echo "DATABASE_URL present: $(if [ -n \"$DATABASE_URL\" ]; then echo YES; else echo NO; fi)"

echo "Creating database tables..."
python -c "
import os, importlib
from app.infrastructure.database.base import Base
from sqlalchemy import create_engine

# Use DATABASE_URL directly if available, otherwise construct from DB_* vars
db_url = os.environ.get('DATABASE_URL', '')
if not db_url:
    from app.core.config import get_settings
    db_url = get_settings().db.sync_dsn
# Replace asyncpg with psycopg2 for sync connection
db_url = db_url.replace('+asyncpg', '+psycopg2')

print(f'Connecting to database...')

# Import all models to register with Base.metadata
modules = [
    'app.modules.auth.infrastructure.models.auth_models',
    'app.modules.tenant.infrastructure.models.tenant_models',
    'app.modules.staff.infrastructure.models.staff_models',
    'app.modules.customer.infrastructure.models.customer_models',
    'app.modules.scheduling.infrastructure.models.scheduling_models',
    'app.modules.payment.infrastructure.models.payment_models',
    'app.modules.notification.infrastructure.models.notification_models',
    'app.modules.analytics.infrastructure.models.analytics_models',
    'app.modules.site.infrastructure.models.site_models',
]
for mod in modules:
    try:
        importlib.import_module(mod)
    except Exception as e:
        print(f'Warning: could not import {mod}: {e}')

engine = create_engine(db_url)
Base.metadata.create_all(engine)
print('Tables created successfully')
engine.dispose()
"

echo "Starting server..."
exec uvicorn app.presentation.api.app:create_app --factory --host 0.0.0.0 --port "${PORT:-8000}"
