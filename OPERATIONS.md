# OPERATIONS.md — AGENDA OS Operations Guide

## 📊 Monitoramento

### UptimeRobot (gratuito)
```bash
# URLs monitoradas:
https://agendaos.com.br/api/v1/health     # API
https://agendaos.com.br                    # Frontend
https://admin.agendaos.com.br              # Admin

# Alertas configurados:
- E-mail: alertas@seudominio.com
- Telegram: @AgendaOSBot
```

### Logs

```bash
# Logs em tempo real
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml logs -f --tail=100 nginx

# Filtrar erros
docker compose logs backend 2>&1 | grep -i error

# Logs de acesso Nginx
docker compose exec nginx cat /var/log/nginx/access.log
```

### Métricas (Prometheus + Grafana)

```bash
# Métricas disponíveis em:
http://localhost:9090  # Prometheus (se profile: monitoring)
http://localhost:3000  # Grafana (se profile: monitoring)
```

---

## 🔧 Manutenção de Rotina

### Diária
- [ ] Verificar health: `curl https://agendaos.com.br/api/v1/health`
- [ ] Verificar backups: `ls -lh /opt/backups/`
- [ ] Checar alertas do UptimeRobot

### Semanal
- [ ] Verificar uso de disco: `df -h`
- [ ] Limpar logs antigos: `docker system prune -f`
- [ ] Verificar certificado SSL: `certbot certificates`

### Mensal
- [ ] Testar restauração de backup (ver BACKUP.md)
- [ ] Atualizar dependências: `pip list --outdated`
- [ ] Revisar logs de segurança: `grep "failed_login" logs/`
- [ ] Rotacionar chaves JWT: atualizar `.env.production` + redeploy

### Trimestral
- [ ] Pentest básico: OWASP ZAP scan
- [ ] Revisão de acessos: remover usuários inativos
- [ ] Atualizar Docker images base

---

## 📈 Escalabilidade

### Sinais para Escalar

| Métrica | Alerta | Ação |
|---------|--------|------|
| CPU > 80% | Escalar vertical | Aumentar vCPU |
| RAM > 80% | Escalar vertical | Aumentar RAM |
| Disco > 80% | Adicionar disco | Limpar ou expandir |
| Latência API > 500ms | Otimizar | Cache Redis, query tuning |
| Conexões DB > 80% pool | Aumentar pool | `DB_POOL_SIZE` |

### Escala Vertical (Single Server)

```bash
# 1. Fazer snapshot/backup
# 2. Upgrade do plano no provedor
# 3. Ajustar limites no docker-compose.prod.yml:
deploy:
  resources:
    limits:
      memory: 4G
      cpus: "3.0"
# 4. Aumentar workers: WORKERS=8
# 5. Redeploy
```

### Escala Horizontal (Multi-Server)

```yaml
# Para quando single server não for suficiente:
# - Load balancer: Nginx/HAProxy na frente
# - PostgreSQL: RDS ou replica
# - Redis: Cluster ou ElastiCache
# - Sessões: Redis compartilhado
# - Uploads: S3/R2
```

---

## 🚨 Comandos de Emergência

```bash
# Reiniciar tudo
docker compose -f docker-compose.prod.yml restart

# Modo manutenção
docker compose -f docker-compose.prod.yml stop backend worker
# ... manutenção ...
docker compose -f docker-compose.prod.yml start backend worker

# Rollback (última imagem estável)
docker compose -f docker-compose.prod.yml up -d --no-build

# Matar e recriar containers
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d

# Verificar uso de recursos
docker stats --no-stream
```

---

## 📞 Contatos de Emergência

| Serviço | Status Page | Suporte |
|---------|-------------|---------|
| Hostinger/DigitalOcean | status page do provedor | Ticket/chat |
| Stripe | status.stripe.com | 24/7 chat |
| Mercado Pago | status.mercadopago.com.br | Ticket |
| Resend | status.resend.com | E-mail |
| Cloudflare | cloudflarestatus.com | Ticket |

---

## 🔄 Health Check Endpoints

```bash
# API principal
GET  /api/v1/health
GET  /api/v1/health/live    # Liveness probe
GET  /api/v1/health/ready   # Readiness probe

# Agentes
GET  /api/v1/agents/health
GET  /api/v1/agents/{id}/status

# Exemplo de resposta:
{
  "agents": {
    "and": {"status": "healthy", "latency_ms": 2.3},
    "hermes": {"status": "healthy", "latency_ms": 1.8}
  },
  "total": 5,
  "healthy": 5
}
```
