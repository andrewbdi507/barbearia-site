# CHECKLIST GO LIVE — Barbershop SaaS

**Status:** ⬜ Pendente | 🟡 Em Progresso | ✅ Concluído | ⚠️ Parcial | ❌ Não Iniciado

---

## 1. INFRAESTRUTURA

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 1.1 | Servidor provisionado (4 vCPU, 8 GB+) | ⬜ | |
| 1.2 | Docker 26+ instalado | ⬜ | |
| 1.3 | Docker Compose v2 instalado | ⬜ | |
| 1.4 | Firewall configurado (ports 80, 443 apenas) | ⬜ | |
| 1.5 | Fail2ban ou similar configurado | ⬜ | |
| 1.6 | Backup automático agendado (cron) | ⬜ | |
| 1.7 | Monitoramento de disco configurado | ⬜ | |

---

## 2. BANCO DE DADOS

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 2.1 | PostgreSQL 16 rodando | ✅ | docker-compose.prod.yml |
| 2.2 | Extensions habilitadas (uuid-ossp, pgcrypto, citext) | ✅ | init-db.sql |
| 2.3 | RLS ativo por tenant | ✅ | |
| 2.4 | Índices criados para queries frequentes | ✅ | |
| 2.5 | Pool de conexões configurado (20 + 10 overflow) | ✅ | |
| 2.6 | Migrations executadas (`alembic upgrade head`) | ⚠️ | Precisa corrigir env.py para `app/` |
| 2.7 | Seed de planos iniciais executado | ⬜ | Starter, Pro, Premium, Enterprise |
| 2.8 | WAL archiving configurado | ⬜ | |
| 2.9 | Backup diário verificado (restore test) | ⬜ | |

---

## 3. REDIS

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 3.1 | Redis 7 rodando | ✅ | docker-compose.prod.yml |
| 3.2 | Senha forte configurada | ⬜ | |
| 3.3 | Persistência (AOF + RDB) habilitada | ✅ | |
| 3.4 | Max memory definido (1 GB) | ✅ | |
| 3.5 | Monitoramento ativo (redis_exporter ou similar) | ⬜ | |

---

## 4. WORKERS & SCHEDULER

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 4.1 | Worker rodando (2+ replicas) | ✅ | docker-compose.prod.yml |
| 4.2 | Scheduler rodando | ✅ | docker-compose.prod.yml |
| 4.3 | Filas processando sem erros | ⬜ | Verificar após deploy |
| 4.4 | DLQ monitorada | ⬜ | |
| 4.5 | Cron jobs configurados (backup, cleanup) | ⬜ | |

---

## 5. STORAGE

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 5.1 | Provider configurado (S3/R2) | ⬜ | |
| 5.2 | Bucket criado com versionamento | ⬜ | |
| 5.3 | CORS configurado no bucket | ⬜ | |
| 5.4 | Lifecycle policies (Glacier/IA para antigos) | ⬜ | |
| 5.5 | Credenciais configuradas (IAM com mínimo privilégio) | ⬜ | |

---

## 6. SSL / DOMÍNIO / DNS

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 6.1 | Domínio registrado | ⬜ | |
| 6.2 | DNS configurado (A records: @, api, admin, grafana) | ⬜ | |
| 6.3 | Cloudflare configurado (DNS + proxy) | ⬜ | Recomendado |
| 6.4 | SSL ativo (Let's Encrypt ou Cloudflare) | ⬜ | |
| 6.5 | Auto-renew SSL configurado (certbot cron) | ⬜ | |
| 6.6 | Redirect HTTP → HTTPS | ⬜ | |
| 6.7 | WWW → non-WWW redirect | ⬜ | |
| 6.8 | SPF, DKIM, DMARC para emails transacionais | ⬜ | |

---

## 7. CDN

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 7.1 | Cloudflare CDN ativo (proxy laranja) | ⬜ | |
| 7.2 | Cache rules para estáticos (CSS, JS, imagens) | ⬜ | |
| 7.3 | DDoS protection ativo | ⬜ | Cloudflare já provê |
| 7.4 | Bot Fight Mode configurado | ⬜ | |

---

## 8. BACKUPS

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 8.1 | Backup diário automático (2 AM) | ⬜ | Script pronto, cron pendente |
| 8.2 | Backup semanal (Domingo) | ⬜ | |
| 8.3 | Backup mensal (Dia 1) | ⬜ | |
| 8.4 | Retenção: 30d diário, 12sem semanal, 60m mensal | ⬜ | |
| 8.5 | Sync para S3/R2 configurado | ⬜ | |
| 8.6 | Teste de restore realizado | ⬜ | Fazer antes de Go Live |
| 8.7 | Backup de uploads configurado | ⬜ | |

---

## 9. ALERTAS

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 9.1 | Prometheus AlertManager configurado | ✅ | 13 regras |
| 9.2 | Canal Slack configurado | ⬜ | |
| 9.3 | Canal Email configurado | ⬜ | |
| 9.4 | On-call schedule definido | ⬜ | |
| 9.5 | Alertas testados (disparo real) | ⬜ | |

---

## 10. LOGS

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 10.1 | Structlog JSON ativo em produção | ✅ | |
| 10.2 | Loki recebendo logs | ⬜ | Verificar após deploy |
| 10.3 | Promtail configurado | ✅ | |
| 10.4 | Retenção de logs definida (30 dias) | ✅ | Loki config |
| 10.5 | Logs de auditoria registrando | ✅ | audit_logs table |

---

## 11. MONITORAMENTO

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 11.1 | Prometheus scraping | ⬜ | Verificar após deploy |
| 11.2 | Grafana dashboards populados | ⬜ | |
| 11.3 | Node Exporter ativo | ✅ | docker-compose.prod.yml |
| 11.4 | Métricas de negócio registrando | ⬜ | |
| 11.5 | Health endpoints respondendo | ⚠️ | Precisa criar `app.py` |

---

## 12. CI/CD

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 12.1 | Pipeline CI/CD configurado (GitHub Actions) | ✅ | ci-cd.yml + ci.yml |
| 12.2 | Secrets GitHub configurados | ⬜ | |
| 12.3 | Deploy staging automático | ✅ | |
| 12.4 | Deploy produção manual com aprovação | ✅ | |
| 12.5 | Rollback testado | ⬜ | |

---

## 13. SEGURANÇA

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 13.1 | SECRET_KEY forte gerada (64+ chars) | ⬜ | |
| 13.2 | Senha Redis forte | ⬜ | |
| 13.3 | Senha DB forte | ⬜ | |
| 13.4 | HTTPS obrigatório (HSTS) | ⬜ | |
| 13.5 | Security headers (CSP, X-Frame, etc.) | ✅ | Nginx config |
| 13.6 | Rate limiting ativo | ⚠️ | Nginx (básico), Redis pendente |
| 13.7 | CORS restrito a origens conhecidas | ⬜ | |
| 13.8 | Containeres non-root | ✅ | Dockerfiles |
| 13.9 | Secrets fora do repositório | ⚠️ | Templates ok, verificar .env real |
| 13.10 | Scan de vulnerabilidades (Trivy) executado | ⬜ | |
| 13.11 | `.env` no .gitignore | ✅ | |

---

## 14. LGPD

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 14.1 | Termos de uso publicados | ⬜ | |
| 14.2 | Política de privacidade publicada | ⬜ | |
| 14.3 | Consentimento registrado (ConsentModel) | ✅ | |
| 14.4 | Exportação de dados funcional | ⚠️ | Implementado, não testado |
| 14.5 | Anonimização funcional | ⚠️ | Implementado, não testado |
| 14.6 | Deleção funcional | ⚠️ | Implementado, não testado |
| 14.7 | Encarregado de dados (DPO) nomeado | ⬜ | |

---

## 15. CÓDIGO (PRÉ-DEPLOY)

| # | Item | Status | Observação |
|---|------|:------:|------------|
| 15.1 | Bugs críticos corrigidos (C1-C4) | ❌ | **BLOQUEANTE** |
| 15.2 | Entry point `app.py` criado e funcional | ❌ | **BLOQUEANTE** |
| 15.3 | `session.py` criado | ❌ | **BLOQUEANTE** |
| 15.4 | SDKs de pagamento integrados (não stubs) | ❌ | **BLOQUEANTE para clientes pagantes** |
| 15.5 | Testes passando (`pytest -v`) | ⚠️ | Unit ok, integração/E2E placeholder |
| 15.6 | Build Docker funcional | ❌ | **BLOQUEANTE** |
| 15.7 | Alembic migrations sync | ⚠️ | Corrigir env.py |

---

## 16. PÓS-DEPLOY

| # | Item | Status |
|---|------|:------:|
| 16.1 | Smoke test (health + login + booking) | ⬜ |
| 16.2 | Monitorar por 2 horas | ⬜ |
| 16.3 | Verificar alertas (sem falsos positivos) | ⬜ |
| 16.4 | Verificar logs (sem erros) | ⬜ |
| 16.5 | Testar backup/restore no ambiente real | ⬜ |

---

## RESUMO

| Categoria | Pendente | Bloqueante |
|-----------|:--------:|:----------:|
| Infraestrutura | 7 | 0 |
| Banco | 4 | 1 (migrations) |
| Redis | 2 | 0 |
| Workers | 3 | 0 |
| Storage | 5 | 0 |
| SSL/DNS | 8 | 0 |
| Backups | 7 | 0 |
| Alertas | 4 | 0 |
| Logs | 2 | 0 |
| Monitoramento | 4 | 0 |
| Segurança | 5 | 0 |
| LGPD | 5 | 0 |
| Código | 5 | **4 BLOQUEANTES** |
| **TOTAL** | **61** | **5** |

---

## ITENS BLOQUEANTES (Devem ser resolvidos antes do Go Live)

1. ❌ **Criar `app/presentation/api/app.py`** — Entry point da aplicação
2. ❌ **Criar `app/infrastructure/database/session.py`** — Gerenciamento de sessão
3. ❌ **Corrigir `TokenExpiredError` + `jwt_algorithm`** — Auth funcional
4. ❌ **Integrar SDKs de pagamento reais** — Clientes pagantes
5. ⚠️ **Corrigir Alembic para `app/`** — Migrations funcionais

**Tempo estimado para resolver todos os bloqueantes:** 40-50 horas (1 semana)
