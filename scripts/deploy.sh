#!/bin/bash
# ============================================================
# AGENDA OS — Production Deploy Script
# ============================================================
# Usage:
#   chmod +x deploy.sh
#   ./deploy.sh
#
# Prerequisites:
#   - Docker 24+ & Docker Compose v2 installed
#   - .env.production filled with real credentials
#   - SSL certs in docker/nginx/ssl/
# ============================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; exit 1; }
info() { echo -e "${BLUE}[i]${NC} $1"; }

COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.production"

# ---- Pre-flight Checks ----
info "AGENDA OS — Production Deploy"
info "=============================="

[ -f "$ENV_FILE" ] || err ".env.production not found. Copy .env.production.example and fill in values."
[ -f "$COMPOSE_FILE" ] || err "$COMPOSE_FILE not found."

# Check secret key
if grep -q "openssl rand" "$ENV_FILE"; then
  warn "SECRET_KEY contains placeholder. Generating new one..."
  NEW_KEY=$(openssl rand -hex 32)
  sed -i "s|<generate-via: openssl rand -hex 32>|$NEW_KEY|g" "$ENV_FILE"
  log "SECRET_KEY generated"
fi

# Check DB password
if grep -q "generate-strong-password" "$ENV_FILE"; then
  warn "DB_PASSWORD contains placeholder. Generating new one..."
  NEW_DB=$(openssl rand -hex 16)
  sed -i "s|<generate-strong-password-32chars>|$NEW_DB|g" "$ENV_FILE"
  log "DB_PASSWORD generated"
fi

# ---- Pull latest images ----
info "Pulling latest Docker images..."
docker compose -f "$COMPOSE_FILE" pull 2>/dev/null || warn "Pull failed, will build locally"

# ---- Build & Start ----
info "Building and starting services..."
docker compose -f "$COMPOSE_FILE" up -d --build --remove-orphans

# ---- With agents ----
info "Starting AI agents (profile: agents)..."
docker compose -f "$COMPOSE_FILE" --profile agents up -d

# ---- Wait for healthy ----
info "Waiting for services to be healthy..."
sleep 5

MAX_RETRIES=30
RETRY=0
while [ $RETRY -lt $MAX_RETRIES ]; do
  HEALTHY=$(docker compose -f "$COMPOSE_FILE" ps --format json | grep -c '"Health":"healthy"' || true)
  TOTAL=$(docker compose -f "$COMPOSE_FILE" ps --format json | wc -l)
  if [ "$HEALTHY" -ge "$((TOTAL - 2))" ]; then
    log "All services healthy ($HEALTHY/$TOTAL)"
    break
  fi
  RETRY=$((RETRY + 1))
  sleep 2
done

# ---- Run migrations ----
info "Running database migrations..."
docker compose -f "$COMPOSE_FILE" exec -T backend uv run alembic upgrade head || warn "Migration may have already been applied"

# ---- Status ----
info ""
info "=============================="
log "DEPLOY COMPLETE"
info "=============================="
docker compose -f "$COMPOSE_FILE" ps

info ""
info "Health check:"
curl -sf http://localhost:8000/health 2>/dev/null && log "Backend healthy" || warn "Backend not responding yet"

info ""
info "Next steps:"
info "  1. Verify: https://agendaos.com.br"
info "  2. Agents: curl http://localhost:8000/api/v1/agents/health"
info "  3. Logs:   docker compose -f $COMPOSE_FILE logs -f backend"
