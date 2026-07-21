#!/bin/sh
# ============================================================
# AGENDA OS — Startup Script (Render Production)
# ============================================================

set -e

echo "Parsing DATABASE_URL..."
if [ -n "$DATABASE_URL" ]; then
  DB_USER=$(echo "$DATABASE_URL" | sed -n 's|.*://\([^:]*\):.*|\1|p')
  DB_PASSWORD=$(echo "$DATABASE_URL" | sed -n 's|.*://[^:]*:\([^@]*\)@.*|\1|p')
  DB_HOST=$(echo "$DATABASE_URL" | sed -n 's|.*@\([^:/]*\).*|\1|p')
  DB_PORT=$(echo "$DATABASE_URL" | sed -n 's|.*:\([0-9]*\)/.*|\1|p')
  DB_NAME=$(echo "$DATABASE_URL" | sed -n 's|.*/\([^?]*\).*|\1|p')
  export DB_USER DB_PASSWORD DB_HOST DB_PORT DB_NAME
  echo "DB_HOST=$DB_HOST DB_NAME=$DB_NAME"
fi

export PYTHONPATH=/app

echo "Running database migrations..."
python -c "
import importlib
from app.core.config import get_settings
from app.infrastructure.database.base import Base
from sqlalchemy import create_engine

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

settings = get_settings()
engine = create_engine(settings.db.sync_dsn)
Base.metadata.create_all(engine)
print('Tables created successfully')
engine.dispose()
"

echo "Starting server..."
exec uvicorn app.presentation.api.app:create_app --factory --host 0.0.0.0 --port "${PORT:-8000}"
