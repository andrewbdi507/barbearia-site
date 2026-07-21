# ============================================================
# Barbershop SaaS — Production Deploy Checklist
# ============================================================
# Use este checklist antes de cada deploy para produção.

## Pré-Deploy

### Banco de Dados
- [ ] Backup realizado nas últimas 24h
- [ ] Migrations testadas em staging
- [ ] Rollback testado em staging
- [ ] Índices revisados (sem índices faltantes)
- [ ] Conexões pool size adequado
- [ ] WAL archiving ativo

### Redis
- [ ] Senha configurada e forte
- [ ] Max memory definido
- [ ] Persistência (AOF + RDB) habilitada
- [ ] Monitoramento ativo (redis_exporter)

### Workers
- [ ] Filas processando sem backlog
- [ ] DLQ vazia ou monitorada
- [ ] Retry policy configurada
- [ ] Logs de worker sem erros

### Scheduler
- [ ] Cron jobs configurados
- [ ] Backup automático agendado
- [ ] Limpeza de sessões agendada

### Storage
- [ ] Provider configurado (S3/R2)
- [ ] Bucket versioning habilitado
- [ ] CORS configurado
- [ ] Lifecycle policies (objetos antigos → Glacier/IA)

### CDN (Cloudflare)
- [ ] DNS configurado (A records)
- [ ] SSL/TLS: Full (strict)
- [ ] Caching rules para estáticos
- [ ] DDoS protection ativo
- [ ] Firewall rules (rate limiting)

### SSL
- [ ] Certificado válido e não próximo de expirar
- [ ] Auto-renew configurado (certbot)
- [ ] TLS 1.2+ apenas
- [ ] HSTS header presente

### Domínio / DNS
- [ ] Domínio principal resolve para IP correto
- [ ] Subdomínios (api, admin, grafana) configurados
- [ ] WWW → non-WWW redirect
- [ ] TXT records (SPF, DKIM, DMARC) para emails

### Backups
- [ ] Backup automático diário funcionando
- [ ] Retenção configurada (30d diário, 12w semanal, 60m mensal)
- [ ] Sync para S3/R2 funcionando
- [ ] Teste de restore realizado este mês

### Alertas
- [ ] Prometheus alerts configurados
- [ ] Canais de notificação (Slack, Email) testados
- [ ] On-call schedule definido
- [ ] Thresholds calibrados (sem falsos positivos)

### Logs
- [ ] Loki recebendo logs
- [ ] Promtail enviando sem erros
- [ ] Retenção de logs configurada
- [ ] Logs estruturados (JSON) ativos

### Métricas
- [ ] Prometheus scraping sem erros
- [ ] Grafana dashboards populados
- [ ] Métricas de negócio registrando
- [ ] Node exporter ativo

### Segurança
- [ ] Security headers presentes (HSTS, CSP, X-Frame, etc.)
- [ ] Rate limiting ativo
- [ ] CORS restrito a origens conhecidas
- [ ] Secrets não expostos em logs
- [ ] Containeres rodando como non-root
- [ ] Imagens escaneadas (Trivy) — sem CRITICAL/HIGH
- [ ] Dependências auditadas (pip-audit, pnpm audit)
- [ ] `.env` e secrets fora do repositório

### Escalabilidade
- [ ] API replicas ≥ 2
- [ ] Worker replicas ≥ 2
- [ ] Resource limits definidos nos containers
- [ ] Load balancer (Nginx) configurado
- [ ] Health checks em todos os serviços

---

## Deploy

- [ ] Notificar time sobre janela de deploy
- [ ] Backup pre-deploy realizado
- [ ] Deploy blue-green executado
- [ ] Migrations aplicadas sem erro
- [ ] Health checks passando (API + Nginx + Worker + Scheduler)
- [ ] Smoke tests passando
- [ ] Logs sem erros novos

---

## Pós-Deploy

- [ ] Monitorar por 30 minutos
- [ ] Verificar métricas no Grafana (sem degradação)
- [ ] Verificar alertas (sem falsos positivos)
- [ ] Verificar filas (sem backlog)
- [ ] Testar fluxo crítico (login → agendamento → pagamento)
- [ ] Notificar time sobre conclusão
- [ ] Atualizar CHANGELOG

---

## Rollback (se necessário)

- [ ] Identificar versão estável anterior
- [ ] Restaurar imagem Docker anterior
- [ ] Rollback de migrations (se necessário) — `alembic downgrade -1`
- [ ] Restaurar banco do backup pre-deploy (se necessário)
- [ ] Health check pós-rollback
- [ ] Post-mortem: documentar causa

---

## Ambientes (Referência)

| Ambiente | Domínio | CI/CD |
|----------|---------|-------|
| Development | localhost | Manual |
| Testing | CI ephemeral | Automático (PR) |
| Staging | staging.barbershop.local | Automático (main) |
| Production | app.barbershop.com | Manual (workflow_dispatch) |
