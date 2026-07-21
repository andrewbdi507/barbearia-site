#!/usr/bin/env bash
# Barbershop SaaS — Development Quick Start
# ============================================================

set -e

echo "============================================"
echo "  Barbershop SaaS — Quick Start"
echo "============================================"

# 1. Setup environment
echo ""
echo "[1/4] Setting up Python environment..."
python scripts/setup.py

# 2. Start Docker services
echo ""
echo "[2/4] Starting Docker services..."
docker compose up -d

# 3. Wait for services to be healthy
echo ""
echo "[3/4] Waiting for services to be ready..."
sleep 5

# 4. Run migrations
echo ""
echo "[4/4] Running database migrations..."
uv run alembic upgrade head

echo ""
echo "============================================"
echo "  ✅ All services are ready!"
echo ""
echo "  API:         http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo "  Health:      http://localhost:8000/api/v1/health/live"
echo ""
echo "  Start dev server:"
echo "    uv run uvicorn src.presentation.api.app:create_app --factory --reload"
echo "============================================"
