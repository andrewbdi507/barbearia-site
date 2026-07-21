# BACKUP.md — Estratégia de Backup

## Política

| Métrica | Valor |
|---------|-------|
| **RPO** (Recovery Point Objective) | < 5 minutos (WAL) / < 24 horas (Full) |
| **RTO** (Recovery Time Objective) | < 1 hora |
| **Retenção diário** | 30 dias |
| **Retenção semanal** | 12 semanas |
| **Retenção mensal** | 60 meses |
| **Retenção auditoria** | 5 anos (LGPD) |

---

## O Que é Backupeado

| Componente | Método | Frequência | Local |
|------------|--------|------------|-------|
| **PostgreSQL** | `pg_dump` custom format + WAL | Contínuo (WAL) + Diário 2AM (full) | Local + S3/R2 |
| **Uploads/Mídia** | Tar + compress | Diário 3AM | S3/R2 |
| **Configurações** | Git (IaC) | A cada deploy | GitHub |
| **Logs de auditoria** | Incluídos no dump do banco | Diário | Banco + Loki |

### O Que NÃO é Backupeado

| Componente | Motivo |
|------------|--------|
| Sessões (Redis) | Efêmeras (15 min) |
| Cache (Redis) | Reconstruível |
| Arquivos temporários | Efêmeros |
| Build artifacts | Reconstruíveis via CI/CD |

---

## Backup do Banco

### Automático (Cron)

```cron
# Daily 2 AM
0 2 * * * /opt/barbershop/scripts/backup-db.sh daily >> /var/log/barbershop-backup.log 2>&1
```

### Manual

```bash
bash scripts/backup-db.sh manual
bash scripts/backup-db.sh pre-deploy-v1.2.0
```

### Estrutura de Arquivos

```
backups/postgres/
├── daily/
│   └── 2026-07/
│       ├── barbershop_production_2026-07-20_020001_daily.dump.gz
│       ├── barbershop_production_2026-07-21_020001_daily.dump.gz
│       └── ...
├── weekly/
│   ├── barbershop_production_weekly_2026-07-13_020001.dump.gz
│   └── ...
└── monthly/
    ├── barbershop_production_monthly_2026-07-01_020001.dump.gz
    └── ...
```

---

## Backup de Uploads

```bash
bash scripts/backup-uploads.sh
```

Os uploads também devem ter versionamento de bucket habilitado no S3/R2 para proteção contra deleção acidental.

---

## Verificação de Integridade

### Teste de Restauração (Mensal)

```bash
# 1. Restaure o backup mais recente em um banco temporário
docker exec barbershop-prod-postgres createdb -U barbershop barbershop_restore_test

gunzip -c backups/postgres/daily/2026-07/latest.dump.gz | \
    docker exec -i barbershop-prod-postgres \
    pg_restore -U barbershop -d barbershop_restore_test --no-owner

# 2. Verifique contagem de registros
docker exec barbershop-prod-postgres psql -U barbershop -d barbershop_restore_test -c "
    SELECT
        (SELECT COUNT(*) FROM tenants) AS tenants,
        (SELECT COUNT(*) FROM users) AS users,
        (SELECT COUNT(*) FROM bookings) AS bookings,
        (SELECT COUNT(*) FROM payments) AS payments;
"

# 3. Remova banco de teste
docker exec barbershop-prod-postgres dropdb -U barbershop barbershop_restore_test
```

### Monitoramento

O Prometheus alerta se o último backup foi há mais de 24h:
```
ALERT BackupFailed
  backup_last_success_timestamp < (time() - 86400)
```

---

## Sync para Cloud

### AWS S3

```bash
# Configurar credenciais
aws configure

# Sync automático incluso no script backup-db.sh
BACKUP_S3_BUCKET=barbershop-backups-prod bash scripts/backup-db.sh
```

### Cloudflare R2

```bash
# Configurar rclone
rclone config

# Sync automático incluso no script backup-db.sh
BACKUP_R2_REMOTE=r2:barbershop-backups bash scripts/backup-db.sh
```

---

## Disaster Recovery Rápido

```bash
# Do zero em um novo servidor:
# 1. Provisionar servidor + Docker
# 2. Clonar repositório
# 3. Configurar .env.production
# 4. Restaurar banco do backup mais recente
bash scripts/restore-db.sh backups/postgres/daily/2026-07/latest.dump.gz
# 5. Iniciar serviços
docker compose -f docker-compose.prod.yml up -d
```
