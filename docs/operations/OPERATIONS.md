# OPERATIONS.md — Guia de Operações

## Visão Geral

Este documento descreve a operação diária da plataforma Barbershop SaaS em produção.

---

## Estrutura de Arquivos (Servidor)

```
/opt/barbershop/
├── docker-compose.prod.yml      # Orquestração de produção
├── docker-compose.staging.yml    # Orquestração de staging
├── config/
│   ├── environments/
│   │   ├── .env.dev              # Template desenvolvimento
│   │   ├── .env.staging          # Staging
│   │   └── .env.production      # Template produção
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── alerts.yml
│   ├── grafana/
│   │   ├── datasources/
│   │   └── dashboards/
│   ├── loki/
│   │   └── loki-config.yml
│   └── promtail/
│       └── promtail-config.yml
├── scripts/
│   ├── backup-db.sh
│   ├── restore-db.sh
│   └── backup-uploads.sh
├── backups/
│   ├── postgres/
│   │   ├── daily/
│   │   ├── weekly/
│   │   └── monthly/
│   └── uploads/
├── storage/
│   └── uploads/                  # Uploads locais (fallback)
└── config/ssl/                   # Certificados SSL
```

---

## Arquitetura de Containers

```
barbershop-prod-net (bridge)
├── barbershop-prod-postgres     :5432 (127.0.0.1 only)
├── barbershop-prod-redis        :6379 (127.0.0.1 only)
├── barbershop-prod-backend      :8000 (127.0.0.1 only)  x2
├── barbershop-prod-worker                                x2
├── barbershop-prod-scheduler                             x1
├── barbershop-prod-nginx        :80, :443 (public)
├── barbershop-prod-prometheus   :9090 (127.0.0.1 only)
├── barbershop-prod-grafana      :3000 (127.0.0.1 only)
├── barbershop-prod-loki         :3100 (127.0.0.1 only)
├── barbershop-prod-promtail
└── barbershop-prod-node-exporter :9100 (127.0.0.1 only)
```

---

## Comandos de Operação

### Startup

```bash
# Iniciar tudo
docker compose -f docker-compose.prod.yml up -d

# Iniciar serviço específico
docker compose -f docker-compose.prod.yml up -d backend
```

### Shutdown

```bash
# Parar tudo (mantém volumes)
docker compose -f docker-compose.prod.yml down

# Parar serviço específico
docker compose -f docker-compose.prod.yml stop backend
```

### Update

```bash
# Pull + restart (zero-downtime via rolling update)
docker compose -f docker-compose.prod.yml pull backend
docker compose -f docker-compose.prod.yml up -d --scale backend=4 --no-recreate backend
sleep 20
docker compose -f docker-compose.prod.yml up -d --scale backend=2 backend
```

---

## Monitoramento

### Dashboards

| Dashboard | URL | Acesso |
|-----------|-----|--------|
| Operations | http://localhost:3000/d/barbershop-operations | admin / `.env` |
| Prometheus | http://localhost:9090 | Interno |

### Health Endpoints

| Endpoint | Uso |
|----------|-----|
| `GET /health` | Status completo (DB, Redis, migrations) |
| `GET /health/live` | Liveness probe (K8s/Docker) |
| `GET /health/ready` | Readiness probe |
| `GET /metrics` | Prometheus metrics |

---

## Backup e Restore

### Backup Manual

```bash
bash scripts/backup-db.sh manual
bash scripts/backup-uploads.sh
```

### Restore

```bash
bash scripts/restore-db.sh backups/postgres/daily/2026-07/backup_file.dump.gz
```

### Teste de Restore (Mensal)

```bash
# Em banco separado
docker exec barbershop-prod-postgres createdb -U barbershop barbershop_restore_test
gunzip -c backups/postgres/daily/2026-07/latest.dump.gz | \
    docker exec -i barbershop-prod-postgres pg_restore -U barbershop -d barbershop_restore_test
# Verificar...depois:
docker exec barbershop-prod-postgres dropdb -U barbershop barbershop_restore_test
```

---

## Manutenção Programada

### Diária

- [ ] Verificar health endpoints
- [ ] Verificar alertas Grafana
- [ ] Verificar logs de erro
- [ ] Confirmar backups noturnos

### Semanal

- [ ] Revisar métricas de negócio
- [ ] Verificar filas DLQ
- [ ] Verificar espaço em disco
- [ ] Revisar logs de segurança

### Mensal

- [ ] Teste de restore de backup
- [ ] Scan de vulnerabilidades (Trivy, pip-audit)
- [ ] Verificar expiração SSL
- [ ] Revisar capacity (CPU, RAM, disco)
- [ ] Rotacionar secrets (se aplicável)
- [ ] Atualizar dependências (após testar em staging)

### Trimestral

- [ ] Simulação de disaster recovery
- [ ] Revisão de acessos ao servidor
- [ ] Atualização de documentação
- [ ] Teste de carga (k6/locust)

---

## Capacity Planning

### Sinais de Alerta

| Métrica | Threshold | Ação |
|---------|:---------:|------|
| CPU > 70% (sustentado) | ⚠️ | Escalar API ou upgrade VPS |
| RAM > 80% | ⚠️ | Aumentar RAM ou otimizar |
| Disco < 20% livre | ⚠️ | Expandir disco ou limpar |
| DB > 100 conexões | ⚠️ | Aumentar pool ou otimizar queries |
| P95 latency > 1s | ⚠️ | Investigar gargalo |
| Backup > 1h | ⚠️ | Otimizar ou particionar |

### Escala Vertical (mesmo servidor)

```bash
# Aumentar workers
# Editar .env.production:
API_WORKERS=8
API_REPLICAS=4

docker compose -f docker-compose.prod.yml up -d backend
```

### Escala Horizontal (novos servidores — fase 2)

- Adicionar nós ao Docker Swarm
- Separar banco para instância dedicada (RDS/Cloud SQL)
- Separar Redis (ElastiCache/Memorystore)

---

## Troubleshooting Rápido

| Sintoma | Verificar |
|---------|-----------|
| API lenta | `docker stats`, P95 latency no Grafana, slow queries |
| Erro 500 | `docker logs barbershop-prod-backend --tail 200 \| grep ERROR` |
| Banco lento | `SELECT * FROM pg_stat_activity WHERE state='active'` |
| Redis cheio | `docker exec ... redis-cli INFO memory` |
| Worker parado | `docker logs barbershop-prod-worker --tail 100` |
| Upload falhando | Verificar conectividade S3/R2, espaço em disco |
| Certificado expirado | `certbot certificates`, `certbot renew` |
| Muito 429 | Ajustar rate limits ou verificar ataque |

---

## Upgrade de Versão (Major)

```bash
# 1. Anunciar janela de manutenção
# 2. Backup pre-deploy
bash scripts/backup-db.sh pre-upgrade-v2.0.0

# 3. Deploy em staging primeiro
# (CI/CD já faz isso automaticamente)

# 4. Deploy produção com blue-green
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d --scale backend=4 backend
sleep 30

# 5. Executar migrations
docker compose -f docker-compose.prod.yml run --rm backend uv run alembic upgrade head

# 6. Health check
curl -f http://localhost:8000/health

# 7. Finalizar
docker compose -f docker-compose.prod.yml up -d --scale backend=2 backend

# 8. Monitorar por 30 minutos
```
