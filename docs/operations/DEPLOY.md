# DEPLOY.md — Guia de Deploy

## Visão Geral

Este documento descreve o processo completo de deploy da plataforma Barbershop SaaS em todos os ambientes.

---

## Ambientes

| Ambiente | Domínio | Deploy | Banco | Observabilidade |
|----------|---------|--------|-------|-----------------|
| **Development** | localhost | Manual (`docker compose up`) | `barbershop_dev` | Logs no terminal |
| **Testing** | CI only | Automático (GitHub Actions) | Ephemeral | CI logs |
| **Staging** | staging.barbershop.local | Automático (push → main) | `barbershop_staging` | Grafana + Prometheus |
| **Production** | app.barbershop.com | Manual (workflow dispatch) | `barbershop_production` | Full stack |

---

## Pré-Requisitos (Produção)

### Servidor
- Linux (Ubuntu 22.04+ recomendado)
- 4+ vCPU, 8+ GB RAM
- 50+ GB SSD
- Docker 26+ + Docker Compose v2

### DNS / Rede
- Domínio configurado (Cloudflare recomendado)
- SSL: Cloudflare (edge) + Let's Encrypt (origin)
- Portas: 80, 443 (públicas); 5432, 6379 (localhost only)

### Serviços Externos
- AWS S3 / Cloudflare R2 (uploads + backups)
- Resend / SendGrid (emails transacionais)
- WhatsApp Cloud API (notificações)
- MercadoPago / Stripe (pagamentos)

---

## Setup Inicial (Primeiro Deploy)

```bash
# 1. Clone o repositório
git clone https://github.com/barbershop-saas/barbershop-saas.git /opt/barbershop
cd /opt/barbershop

# 2. Copie e configure o .env de produção
cp config/environments/.env.production config/environments/.env.production.local
# Edite todas as variáveis marcadas como <fill-from-secret-manager>
nano config/environments/.env.production.local

# 3. Gere SECRET_KEY forte
python3 -c "import secrets; print(secrets.token_hex(32))"
# Cole o valor em SECRET_KEY

# 4. Crie diretórios de dados
mkdir -p backups/postgres/{daily,weekly,monthly}
mkdir -p backups/uploads
mkdir -p storage/uploads
mkdir -p config/ssl

# 5. Configure SSL (Let's Encrypt)
certbot certonly --standalone -d app.barbershop.com -d api.barbershop.com
cp /etc/letsencrypt/live/app.barbershop.com/fullchain.pem config/ssl/
cp /etc/letsencrypt/live/app.barbershop.com/privkey.pem config/ssl/

# 6. Inicie o banco primeiro
docker compose -f docker-compose.prod.yml up -d postgres redis
sleep 10

# 7. Execute migrations
docker compose -f docker-compose.prod.yml run --rm backend \
    uv run alembic upgrade head

# 8. Seed de dados iniciais
docker compose -f docker-compose.prod.yml run --rm backend \
    uv run python -m app.infrastructure.seeds.plans

# 9. Inicie todos os serviços
docker compose -f docker-compose.prod.yml up -d

# 10. Verifique saúde
curl http://localhost:8000/health/live
curl http://localhost:80/health
```

---

## Deploy Diário (Atualização)

```bash
cd /opt/barbershop

# Pull latest images
docker compose -f docker-compose.prod.yml pull backend worker scheduler

# Rolling update (zero-downtime)
docker compose -f docker-compose.prod.yml up -d \
    --scale backend=4 --no-recreate backend
sleep 20

# Verify new instances
curl -f http://localhost:8000/health/live

# Scale back
docker compose -f docker-compose.prod.yml up -d \
    --scale backend=2 backend

# Cleanup old images
docker image prune -af --filter "until=48h"
```

---

## Rollback

```bash
# 1. Liste versões disponíveis
docker image ls ghcr.io/barbershop-saas/backend

# 2. Altere a tag no .env
IMAGE_TAG=<versão-anterior>

# 3. Redeploy
docker compose -f docker-compose.prod.yml up -d backend worker scheduler

# 4. Se necessário, restaure banco
bash scripts/restore-db.sh backups/postgres/daily/.../dump.gz
```

---

## CI/CD Pipeline

O pipeline GitHub Actions é definido em `.github/workflows/ci-cd.yml`:

```
Push/PR → Quality (lint, type, security) → Tests (unit, integration, e2e)
  └─ main → Build Images → Deploy Staging (auto)
       └─ manual → Deploy Production
```

### Secrets necessários no GitHub:
- `STAGING_HOST`, `STAGING_USER`, `STAGING_SSH_KEY`
- `PROD_HOST`, `PROD_USER`, `PROD_SSH_KEY`
- `SLACK_WEBHOOK` (opcional)
- `GITHUB_TOKEN` (automático)

---

## Comandos Rápidos

```bash
# Desenvolvimento
make up                    # Inicia dev completo
make logs-backend          # Logs do backend

# Staging
docker compose -f docker-compose.staging.yml up -d
docker compose -f docker-compose.staging.yml logs -f backend

# Produção
docker compose -f docker-compose.prod.yml ps          # Status
docker compose -f docker-compose.prod.yml restart backend  # Restart API
docker compose -f docker-compose.prod.yml exec backend bash  # Shell

# Backup
bash scripts/backup-db.sh manual
bash scripts/restore-db.sh backups/postgres/daily/2026-07/...

# Migrations
docker compose -f docker-compose.prod.yml run --rm backend uv run alembic upgrade head
docker compose -f docker-compose.prod.yml run --rm backend uv run alembic downgrade -1  # Rollback
```
