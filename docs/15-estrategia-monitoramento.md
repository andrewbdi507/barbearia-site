# 15 — Estratégia de Monitoramento

---

## 15.1 Health Checks

### Níveis de Health Check

| Nível | Endpoint | Verifica | Usado por |
|-------|----------|----------|-----------|
| **Liveness** | `/health/live` | Processo está rodando | Kubernetes (restart se falhar) |
| **Readiness** | `/health/ready` | DB, Redis, dependências OK | Kubernetes (remove do load balancer se falhar) |
| **Deep** | `/health/deep` | Todas as dependências + queries de teste | Monitoramento externo |

### O que cada serviço verifica no readiness:

| Serviço | Verificações |
|---------|-------------|
| API (todos) | PostgreSQL ping, Redis ping |
| Scheduler | PostgreSQL ping + query no booking mais recente |
| Notification | Redis ping + conectividade WhatsApp API |
| Payment | PostgreSQL ping + conectividade gateway (cacheada) |
| Media | PostgreSQL ping + S3 bucket accessible |

---

## 15.2 SLI / SLO / SLA

### SLI (Service Level Indicators) — O que medimos

| SLI | Definição | Como Medir |
|-----|-----------|------------|
| **Availability** | % de requests com status != 5xx | Prometheus: `http_requests_total{status!~"5.."}` / total |
| **Latency** | P95 de duração de requests | Prometheus: `histogram_quantile(0.95, http_request_duration_seconds)` |
| **Error Rate** | % de requests com erro 5xx | Prometheus: rate de 5xx |
| **Throughput** | Requests por segundo | Prometheus: `rate(http_requests_total[5m])` |

### SLO (Service Level Objectives) — Metas internas

| SLI | SLO (MVP) | SLO (V1+) | SLO (V2+) |
|-----|:---------:|:---------:|:---------:|
| Availability | 99.5% | 99.9% | 99.95% |
| Latency P95 | < 500ms | < 300ms | < 200ms |
| Error Rate | < 1% | < 0.5% | < 0.1% |

### SLA (Service Level Agreement) — Compromisso com cliente

| Métrica | SLA | Penalidade |
|---------|-----|------------|
| Uptime mensal | ≥ 99.5% | Crédito proporcional ao downtime |
| Tempo de resposta (suporte) | < 24h (Business) / < 4h (Enterprise) | Crédito |

---

## 15.3 Alertas

### Configuração: AlertManager + Grafana Alerts

### Regras de Alerta

| Alerta | Condição | Severidade | Canal |
|--------|----------|------------|-------|
| **Service Down** | Liveness falha por > 2 min | Crítico | Telegram + E-mail |
| **High Error Rate** | Error rate > 1% por 5 min | Crítico | Telegram |
| **High Latency** | P95 > 1s por 10 min | Alerta | Telegram |
| **DB Connection Pool Exhausted** | Conexões ativas > 80% do pool | Alerta | Telegram |
| **Redis Memory > 80%** | Memória usada > 80% | Alerta | Telegram |
| **Disk > 85%** | Disco do servidor > 85% | Alerta | Telegram |
| **SSL Expiry < 7 days** | Certificado expira em < 7 dias | Alerta | E-mail |
| **Backup Failed** | Último backup > 25h | Crítico | Telegram + E-mail |
| **Tenant spike de erros** | Erros de 1 tenant > 10x média | Alerta | Telegram |
| **Cross-tenant access detected** | Tentativa de acesso cross-tenant | Crítico | Telegram (imediato) |
| **Payment gateway down** | Falha consecutiva > 5 min | Crítico | Telegram |
| **Notification failure rate** | > 10% de falhas por 15 min | Alerta | Telegram |

### Canais de Notificação

| Prioridade | Canal |
|------------|-------|
| Crítico | Telegram (notificação imediata) |
| Alerta | Telegram |
| Informativo | E-mail (resumo diário) |

### On-Call (Futuro, quando houver equipe)

- Rotação de plantão via PagerDuty / OpsGenie
- Escalação: Dev → CTO (se não responder em 15 min)

---

## 15.4 Monitoramento de Negócio (SaaS Metrics)

Além da saúde técnica, monitoramos a saúde do negócio:

| Métrica | Limiar de Alerta |
|---------|-----------------|
| MRR caiu > 5% vs semana anterior | ⚠️ Investigar |
| Churn > 10% em um mês | ⚠️ Investigar |
| Novos trials < 5 em uma semana | ⚠️ Marketing |
| Taxa de conversão trial → pago < 20% | ⚠️ Produto/Onboarding |
| Tenant sem agendamentos > 7 dias | ⚠️ Risco de churn |

---

## 15.5 Monitoramento Sintético

### O que é testado

| Teste | Frequência | De onde |
|-------|-----------|---------|
| Site público carrega | A cada 5 min | Cloudflare / UptimeRobot |
| Fluxo de agendamento (simulado) | A cada 15 min | Script externo |
| API responde (health) | A cada 1 min | Prometheus blackbox exporter |
| SSL válido | A cada 1 hora | Cloudflare |
| DNS resolve | A cada 5 min | Cloudflare |

### Script de Agendamento Sintético

Um script externo que, a cada 15 minutos:
1. Acessa site de um tenant de teste
2. Consulta serviços disponíveis (API)
3. Consulta horários disponíveis (API)
4. Cria um agendamento de teste
5. Cancela o agendamento de teste
6. Reporta sucesso/falha + duração de cada etapa

Isso valida o fluxo completo do ponto de vista do cliente.

---

## 15.6 Dashboards de Monitoramento

### Status Page Pública (V1+)

Uma página pública (ex: `status.barbersaas.com.br`) mostrando:
- Status atual: 🟢 Operacional / 🟡 Degradado / 🔴 Indisponível
- Histórico de incidentes (últimos 90 dias)
- Uptime atual (%)

Ferramenta: **BetterStack** (free tier) ou **Grafana Cloud Status Page**.

---

## 15.7 Rotina de Verificação (Diária)

Todo dia, o CTO/Dev verifica:

- [ ] Alertas nas últimas 24h
- [ ] Dashboard de erros (Sentry)
- [ ] Dashboard de saúde (Grafana)
- [ ] Logs de segurança (cross-tenant access?)
- [ ] Backup executado com sucesso
- [ ] Faturamento do dia (tendência)

---

> **Princípio:** Monitoramento sem alerta é inútil. Alerta sem ação é ruído. Cada alerta deve ser acionável — se você não vai fazer nada ao recebê-lo, ele não deveria existir. Comece com poucos alertas de alta qualidade e refine ao longo do tempo.
