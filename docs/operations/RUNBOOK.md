# RUNBOOK.md — Runbook Operacional

## Propósito

Este runbook contém procedimentos operacionais do dia-a-dia para a plataforma Barbershop SaaS.
Para emergências, consulte [RECOVERY.md](./RECOVERY.md).

---

## Índice

1. [Acesso ao Servidor](#1-acesso-ao-servidor)
2. [Verificação de Saúde](#2-verificação-de-saúde)
3. [Gestão de Serviços](#3-gestão-de-serviços)
4. [Logs e Debugging](#4-logs-e-debugging)
5. [Banco de Dados](#5-banco-de-dados)
6. [Filas e Workers](#6-filas-e-workers)
7. [Cache (Redis)](#7-cache-redis)
8. [SSL e Domínios](#8-ssl-e-domínios)
9. [Procedimentos Comuns](#9-procedimentos-comuns)

---

## 1. Acesso ao Servidor

```bash
# SSH
ssh deploy@app.barbershop.com

# Docker
cd /opt/barbershop
docker compose -f docker-compose.prod.yml ps
```

---

## 2. Verificação de Saúde

```bash
# API
curl http://localhost:8000/health
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready

# Nginx
curl http://localhost:80/health

# Banco
docker exec barbershop-prod-postgres pg_isready

# Redis
docker exec barbershop-prod-redis redis-cli -a "$REDIS_PASSWORD" ping

# Workers (ver fila)
docker exec barbershop-prod-redis redis-cli -a "$REDIS_PASSWORD" LLEN barbershop:queue:default
```

---

## 3. Gestão de Serviços

```bash
# Status de todos
docker compose -f docker-compose.prod.yml ps

# Restart de um serviço
docker compose -f docker-compose.prod.yml restart backend
docker compose -f docker-compose.prod.yml restart worker

# Escalar API
docker compose -f docker-compose.prod.yml up -d --scale backend=4 backend

# Ver uso de recursos
docker stats --no-stream

# Limpar imagens antigas
docker image prune -af --filter "until=48h"
docker system prune -f
```

---

## 4. Logs e Debugging

```bash
# Últimos logs
docker compose -f docker-compose.prod.yml logs --tail=100 backend

# Seguir logs em tempo real
docker compose -f docker-compose.prod.yml logs -f backend worker

# Filtrar por termo
docker compose logs backend 2>&1 | grep "ERROR"

# Logs de um container específico
docker logs barbershop-prod-backend --tail 200 -f

# Logs do nginx
docker logs barbershop-prod-nginx --tail 100

# Logs no Grafana (Loki)
# Abra http://localhost:3000 → Explore → Loki → {service="backend"} |= "ERROR"
```

---

## 5. Banco de Dados

### Conexão

```bash
docker exec -it barbershop-prod-postgres psql -U barbershop -d barbershop_production
```

### Queries Úteis

```sql
-- Tenants ativos
SELECT COUNT(*) FROM tenants WHERE status = 'active';

-- Conexões ativas
SELECT COUNT(*) FROM pg_stat_activity WHERE datname = 'barbershop_production';

-- Tamanho do banco
SELECT pg_size_pretty(pg_database_size('barbershop_production'));

-- Tamanho das tabelas (top 10)
SELECT table_name, pg_size_pretty(pg_total_relation_size(quote_ident(table_name)))
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC
LIMIT 10;

-- Locks ativos
SELECT pid, usename, state, query
FROM pg_stat_activity
WHERE state = 'active' AND wait_event IS NOT NULL;

-- Vacuum (manutenção)
VACUUM ANALYZE;
```

### Migrations

```bash
# Aplicar pendentes
docker compose -f docker-compose.prod.yml run --rm backend uv run alembic upgrade head

# Ver status
docker compose -f docker-compose.prod.yml run --rm backend uv run alembic current

# Rollback (última migration)
docker compose -f docker-compose.prod.yml run --rm backend uv run alembic downgrade -1

# Criar nova migration
cd backend && uv run alembic revision --autogenerate -m "descricao"
```

---

## 6. Filas e Workers

```bash
# Ver tamanho da fila
docker exec barbershop-prod-redis redis-cli -a "$REDIS_PASSWORD" LLEN barbershop:queue:default

# Ver DLQ (dead letter queue)
docker exec barbershop-prod-redis redis-cli -a "$REDIS_PASSWORD" LLEN barbershop:queue:dlq

# Reprocessar DLQ
docker compose -f docker-compose.prod.yml exec backend uv run python -m app.infrastructure.worker.retry_dlq

# Limpar fila (⚠️ cuidado!)
docker exec barbershop-prod-redis redis-cli -a "$REDIS_PASSWORD" DEL barbershop:queue:default
```

---

## 7. Cache (Redis)

```bash
# Conectar
docker exec -it barbershop-prod-redis redis-cli -a "$REDIS_PASSWORD"

# Info
INFO memory
INFO stats

# Keys por tenant
KEYS tenant:*

# Limpar cache de um tenant
DEL tenant:ws_abc123:*

# Limpar todo cache (⚠️ apenas se necessário)
FLUSHDB

# Ver clientes conectados
CLIENT LIST
```

---

## 8. SSL e Domínios

```bash
# Verificar expiração SSL
echo | openssl s_client -servername app.barbershop.com -connect app.barbershop.com:443 2>/dev/null | openssl x509 -noout -dates

# Renovar Let's Encrypt
certbot renew --dry-run   # teste
certbot renew              # renovar

# Após renovar, restart nginx
docker compose -f docker-compose.prod.yml restart nginx
```

---

## 9. Procedimentos Comuns

### Adicionar Novo Tenant (Admin)

```sql
INSERT INTO tenants (id, name, subdomain, status, plan_id, created_at, updated_at)
VALUES (gen_random_uuid(), 'Nome Barbearia', 'subdominio', 'active', '<plan_id>', now(), now());
```

### Bloquear Tenant

```sql
UPDATE tenants SET status = 'suspended' WHERE subdomain = 'subdominio';
```

### Verificar Agendamentos do Dia

```sql
SELECT t.name AS tenant, COUNT(*) AS bookings_today
FROM bookings b
JOIN tenants t ON t.id = b.tenant_id
WHERE b.created_at::date = CURRENT_DATE
GROUP BY t.name
ORDER BY bookings_today DESC;
```

### Verificar Pagamentos do Dia

```sql
SELECT gateway, COUNT(*), SUM(amount_cents) / 100.0 AS total
FROM payments
WHERE created_at::date = CURRENT_DATE AND status = 'paid'
GROUP BY gateway;
```

### Limpar Sessões Expiradas

```bash
docker compose -f docker-compose.prod.yml exec backend uv run python -c "
from app.modules.auth.infrastructure.repositories import RefreshTokenRepository
# Delete expired tokens
"
```

### Atualizar Planos

```bash
docker compose -f docker-compose.prod.yml exec backend uv run python -m app.infrastructure.seeds.plans
```

---

## Plantão

### Checklist Diário

- [ ] Verificar health endpoints
- [ ] Verificar alertas no Grafana
- [ ] Verificar backups (executados com sucesso?)
- [ ] Verificar espaço em disco (`df -h`)
- [ ] Verificar logs de erro (`grep ERROR`)

### Checklist Semanal

- [ ] Revisar métricas de negócio (Grafana)
- [ ] Verificar filas DLQ
- [ ] Testar restore de backup
- [ ] Revisar dependências (`pip-audit`)

### Checklist Mensal

- [ ] Rodar checklist de segurança
- [ ] Verificar expiração de SSL
- [ ] Planejar capacity (tendências de uso)
- [ ] Atualizar documentação se necessário
