# BACKUP.md — AGENDA OS Backup & Recovery

## 📦 Estratégia de Backup

| O Que | Frequência | Retenção | Local |
|-------|-----------|----------|-------|
| Banco PostgreSQL | Diário (2h) | 30 dias | Local + R2 |
| Arquivos (uploads) | Diário | 30 dias | R2 (versionado) |
| Configuração (.env) | Manual | Permanente | 1Password/Vault |

---

## 🔧 Backup Automático

### Configuração

```bash
# 1. Tornar script executável
chmod +x scripts/backup.sh

# 2. Testar manualmente
cd /opt/agendaos
DB_USER=agendaos DB_PASSWORD=xxx DB_NAME=agendaos_prod DB_HOST=localhost DB_PORT=5432 ./scripts/backup.sh

# 3. Agendar no cron (diário 2h)
crontab -e
# Adicionar:
0 2 * * * /opt/agendaos/scripts/backup.sh >> /var/log/agendaos-backup.log 2>&1
```

### Verificar Backups

```bash
ls -lh /opt/backups/
# agendaos_20260721_020001.sql.gz (tamanho varia com dados)

# Integridade
gzip -t /opt/backups/agendaos_20260721_020001.sql.gz && echo "OK"
```

---

## 🔄 Restauração

### Restaurar Banco Completo

```bash
# 1. Parar aplicação
cd /opt/agendaos
docker compose -f docker-compose.prod.yml stop backend worker

# 2. Restaurar
gunzip -c /opt/backups/agendaos_20260721_020001.sql.gz | \
  docker compose -f docker-compose.prod.yml exec -T postgres \
  psql -U agendaos -d agendaos_prod

# 3. Reiniciar
docker compose -f docker-compose.prod.yml start backend worker
```

### Restaurar de Backup no R2

```bash
# Baixar do R2
aws s3 cp s3://agendaos-backups/backups/agendaos_20260721_020001.sql.gz . \
  --endpoint-url https://xxx.r2.cloudflarestorage.com

# Restaurar (mesmo processo acima)
```

### Ponto no Tempo (PITR)

```bash
# Habilitar WAL archiving (postgresql.conf)
wal_level = replica
archive_mode = on
archive_command = 'aws s3 cp %p s3://agendaos-backups/wal/%f --endpoint-url https://xxx.r2.cloudflarestorage.com'

# Restaurar para ponto específico
# recovery.conf:
restore_command = 'aws s3 cp s3://agendaos-backups/wal/%f %p --endpoint-url https://xxx.r2.cloudflarestorage.com'
recovery_target_time = '2026-07-21 14:30:00'
```

---

## ✅ Teste de Restauração (Mensal)

```bash
# 1. Criar banco de teste
docker compose -f docker-compose.prod.yml exec postgres \
  createdb -U agendaos agendaos_restore_test

# 2. Restaurar backup no banco de teste
gunzip -c /opt/backups/$(ls -t /opt/backups/ | head -1) | \
  docker compose -f docker-compose.prod.yml exec -T postgres \
  psql -U agendaos -d agendaos_restore_test

# 3. Verificar integridade
docker compose -f docker-compose.prod.yml exec -T postgres \
  psql -U agendaos -d agendaos_restore_test -c "
    SELECT count(*) as tenants FROM tenants;
    SELECT count(*) as users FROM users;
    SELECT count(*) as bookings FROM bookings;
  "

# 4. Limpar
docker compose -f docker-compose.prod.yml exec postgres \
  dropdb -U agendaos agendaos_restore_test
```

---

## 🚨 Disaster Recovery

### Cenário: Servidor completamente perdido

1. **Provisionar novo servidor** (Hostinger/DigitalOcean)
2. **Instalar Docker** (seguir DEPLOY.md)
3. **Clonar repositório** + configurar `.env.production`
4. **Restaurar banco** do R2 (ver seção Restauração)
5. **Rodar deploy** `./scripts/deploy.sh`
6. **Atualizar DNS** para novo IP
7. **Tempo estimado:** 30-60 minutos

### Cenário: Banco corrompido

1. **Parar aplicação** imediatamente
2. **Restaurar último backup** (ver seção Restauração)
3. **Verificar integridade** com queries de validação
4. **Reiniciar aplicação**
5. **Tempo estimado:** 10-20 minutos
