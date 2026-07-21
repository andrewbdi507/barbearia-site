# RECOVERY.md — Disaster Recovery

## Objetivos

| Métrica | Valor |
|---------|-------|
| **RPO** | < 5 minutos (WAL) |
| **RTO** | < 1 hora |
| **RTO Completo** | < 4 horas (inclui novo servidor) |

---

## Cenários de Falha e Procedimentos

### 1. Falha do Banco de Dados (PostgreSQL)

**Sintomas:**
- API retorna 500 com erros de conexão
- `pg_isready` falha
- Prometheus: `DatabaseDown` alert

**Procedimento:**

```bash
# 1. Verificar status
docker ps -a | grep postgres
docker logs barbershop-prod-postgres --tail 50

# 2. Tentar restart
docker restart barbershop-prod-postgres
sleep 10
docker exec barbershop-prod-postgres pg_isready

# 3. Se corrompido, restaurar do backup
bash scripts/restore-db.sh backups/postgres/daily/$(date +%Y-%m)/latest.dump.gz

# 4. Se WAL estiver ativo, PITR para o ponto mais recente
# (consultar docs PostgreSQL PITR)

# 5. Verificar integridade
docker exec barbershop-prod-postgres psql -U barbershop -d barbershop_production \
    -c "SELECT COUNT(*) FROM tenants; SELECT COUNT(*) FROM bookings WHERE created_at > now() - interval '1 hour';"
```

**Prevenção:**
- WAL archiving contínuo
- Streaming replication (fase 2)
- Backups diários verificados

---

### 2. Falha do Redis

**Sintomas:**
- Cache misses em massa
- Rate limiting ausente (degradação de segurança)
- Filas de worker paradas
- Prometheus: `RedisDown` alert

**Procedimento:**

```bash
# 1. Verificar status
docker logs barbershop-prod-redis --tail 50

# 2. Restart
docker restart barbershop-prod-redis
sleep 5
docker exec barbershop-prod-redis redis-cli -a "$REDIS_PASSWORD" ping

# 3. Se dados corrompidos, limpar e reconstruir
docker stop barbershop-prod-redis
rm -rf /var/lib/docker/volumes/barbershop-prod-redis/_data/*
docker start barbershop-prod-redis
```

**Impacto:** Apenas performance. A API funciona sem Redis (cache misses viram queries diretas). Filas resetam (jobs perdidos são reenfileirados).

---

### 3. Falha do Storage (Uploads)

**Sintomas:**
- Erros 500 ao fazer upload
- Imagens quebradas no site/admin
- Prometheus: alto erro rate em `/api/v1/media/upload`

**Procedimento (S3/R2):**

```bash
# Verificar conectividade
curl -I https://s3.amazonaws.com

# Fallback: usar storage local temporário
# Editar .env.production:
STORAGE_PROVIDER=local
docker compose -f docker-compose.prod.yml restart backend worker

# Quando S3 voltar, migrar arquivos:
aws s3 sync /opt/barbershop/storage/uploads/ s3://bucket/uploads/
```

---

### 4. Falha do Servidor (VPS)

**Sintomas:**
- Tudo offline
- Cloudflare mostra "Origin Down"

**Procedimento (Recuperação Completa):**

```bash
# Em um NOVO servidor:

# 1. Provisionar (Ubuntu 22.04, 4 vCPU, 8 GB)
ssh root@<new-server-ip>

# 2. Instalar dependências
apt update && apt install -y docker.io docker-compose-v2 curl certbot
systemctl enable --now docker

# 3. Clonar repositório
git clone https://github.com/barbershop-saas/barbershop-saas.git /opt/barbershop
cd /opt/barbershop

# 4. Restaurar configuração do backup
# Copie config/environments/.env.production do último backup off-site

# 5. Baixar backup mais recente do S3/R2
aws s3 cp s3://barbershop-backups/postgres/daily/2026-07/latest.dump.gz \
    backups/postgres/daily/2026-07/

# 6. Iniciar banco
docker compose -f docker-compose.prod.yml up -d postgres redis
sleep 15

# 7. Restaurar banco
bash scripts/restore-db.sh backups/postgres/daily/2026-07/latest.dump.gz

# 8. Restaurar uploads
aws s3 sync s3://barbershop-backups/uploads/ storage/uploads/

# 9. Migrations + Seed
docker compose -f docker-compose.prod.yml run --rm backend uv run alembic upgrade head

# 10. Iniciar tudo
docker compose -f docker-compose.prod.yml up -d

# 11. Verificar
curl http://localhost:8000/health/live
curl http://localhost:80/health

# 12. Atualizar DNS para novo IP
# Cloudflare Dashboard → DNS → Update A record
```

**Tempo estimado:** 30-60 minutos (depende do tamanho do backup e velocidade de download).

---

### 5. Falha do Gateway de Pagamento

**Sintomas:**
- Pagamentos falhando
- Webhooks não recebidos

**Procedimento:**

```bash
# Verificar status do gateway
curl https://api.mercadopago.com/health
curl https://api.stripe.com/health

# Verificar webhooks recentes
docker exec barbershop-prod-postgres psql -U barbershop -d barbershop_production -c "
    SELECT gateway, status, created_at
    FROM payment_events
    WHERE created_at > now() - interval '1 hour'
    ORDER BY created_at DESC
    LIMIT 20;
"

# Reprocessar pagamentos pendentes manualmente se necessário
```

---

### 6. Falha de DNS / Domínio

**Sintomas:**
- Site inacessível por domínio
- Acessível por IP direto

**Procedimento:**

```bash
# 1. Verificar propagação DNS
dig app.barbershop.com
nslookup app.barbershop.com

# 2. Verificar Cloudflare
# Dashboard → DNS → Records
# Confirmar que o A record aponta para o IP correto

# 3. Enquanto resolve, acessar via IP:
# http://<server-ip>/health

# 4. Se Cloudflare estiver offline, bypass temporário:
# Mudar nameservers no registrador
```

---

## Runbook de Emergência

### Checklist de Resposta a Incidentes

1. [ ] **Detectar:** Alerta do Prometheus → Slack/Email
2. [ ] **Triar:** Identificar severidade (P1/P2/P3)
3. [ ] **Comunicar:** Status page / Slack interno
4. [ ] **Mitigar:** Aplicar procedimento do cenário acima
5. [ ] **Resolver:** Confirmar que serviço voltou ao normal
6. [ ] **Post-Mortem:** Documentar causa raiz e prevenção

### Contatos de Emergência

| Papel | Contato |
|-------|---------|
| Tech Lead | [preencher] |
| DevOps | [preencher] |
| Security | [preencher] |

---

## Testes de DR

### Trimestral

1. Restaurar backup em ambiente isolado
2. Verificar integridade dos dados
3. Testar failover manual
4. Documentar tempo de recuperação

### Comando de Teste

```bash
# Simular disaster recovery em staging
docker compose -f docker-compose.test.yml up -d postgres-test
bash scripts/restore-db.sh backups/postgres/daily/2026-07/latest.dump.gz
docker compose -f docker-compose.test.yml run --rm backend-test
```
