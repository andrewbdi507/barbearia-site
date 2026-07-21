# 14 — Estratégia de Observabilidade

---

## 14.1 Pilares da Observabilidade

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILIDADE                           │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│  │  METRICS │    │  TRACES  │    │   LOGS   │               │
│  │          │    │          │    │          │               │
│  │ Prometheus│   │  Tempo   │    │  Loki    │               │
│  │          │    │(OpenTel.)│    │          │               │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘               │
│       │               │               │                      │
│       └───────────────┼───────────────┘                      │
│                       │                                      │
│                 ┌─────▼─────┐                                │
│                 │  Grafana   │  ← Unified Visualization      │
│                 └───────────┘                                │
│                                                              │
│  + ALERTS (AlertManager)                                     │
│  + ERROR TRACKING (Sentry)                                   │
│  + UPTIME (Cloudflare / ext)                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 14.2 Métricas (Metrics)

### Stack: Prometheus + Grafana

### Métricas de Aplicação (Golden Signals)

| Sinal | Métrica | Descrição |
|-------|---------|-----------|
| **Latency** | `http_request_duration_seconds` (P50, P95, P99) | Tempo de resposta por endpoint |
| **Traffic** | `http_requests_total` | Volume de requisições por segundo |
| **Errors** | `http_requests_total{status=~"5.."}` | Taxa de erros |
| **Saturation** | `process_cpu_seconds_total`, `process_resident_memory_bytes` | Utilização de recursos |

### Métricas de Negócio

| Métrica | Descrição |
|---------|-----------|
| `bookings_created_total` | Total de agendamentos (por tenant, por período) |
| `bookings_cancelled_total` | Total de cancelamentos |
| `payments_succeeded_total` | Pagamentos confirmados (por gateway) |
| `payments_amount_reais` | Volume financeiro processado |
| `tenants_active_total` | Tenants ativos na plataforma |
| `users_logged_in` | Usuários logados (gauge, snapshot) |
| `notifications_sent_total` | Notificações enviadas (por canal) |
| `notifications_failed_total` | Falhas de notificação |

### Métricas de Infraestrutura

| Métrica | Descrição |
|---------|-----------|
| CPU, memória, disco (por container) | Saúde dos serviços |
| PostgreSQL: conexões ativas, locks, replication lag | Saúde do banco |
| Redis: memória usada, hit rate, connected clients | Saúde do cache |
| S3: bytes stored, requests, erros | Saúde do storage |

---

## 14.3 Tracing Distribuído

### Stack: OpenTelemetry + Tempo (Grafana)

Cada request que entra no sistema gera um **trace ID** único, propagado entre todos os serviços:

```
Request: POST /api/v1/bookings
Trace ID: abc123def456

┌─────────────────────────────────────────────────────┐
│ API Gateway (50ms)                                   │
│   ├── Auth Middleware (10ms)                         │
│   ├── Tenant Resolution (5ms)                        │
│   └── Proxy to BFF (2ms)                             │
│                                                      │
│ BFF Public (120ms)                                   │
│   ├── Validate Input (5ms)                           │
│   ├── Scheduler Service (80ms)                       │
│   │   ├── Check Availability (30ms)                  │
│   │   ├── Create Booking (25ms)                      │
│   │   └── Emit Event (5ms)                           │
│   └── Format Response (2ms)                          │
│                                                      │
│ Notification Service (async, 200ms)                  │
│   ├── Consume Event (10ms)                           │
│   ├── Send WhatsApp (150ms)                          │
│   └── Send Email (40ms)                              │
└─────────────────────────────────────────────────────┘

Total Time (sync): 172ms
Total Time (async): +200ms (background)
```

### Benefícios
- Identificar gargalos de performance
- Debugging de requests lentos
- Visualizar cascata de chamadas entre serviços
- Medir latência de cada etapa

---

## 14.4 Logs

Stack: Loki + Promtail (detalhado no documento 12 — Estratégia de Logs).

### Integração com Tracing

Cada log carrega `trace_id` e `request_id`, permitindo correlacionar:
- Um erro no log → trace completo → métricas daquele endpoint

```
log: "booking.create failed: professional not found"
trace_id: abc123 → mostra todo o fluxo da requisição
metrics: mostra que 0.5% dos bookings falham com esse erro
```

---

## 14.5 Dashboards

### Dashboard 1: Visão Executiva (Negócio)

```
┌─────────────────────────────────────────────────────────┐
│            BARBERSAAS — VISÃO EXECUTIVA                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Tenants  │  │   MRR    │  │ Churn    │  │ Novos    │ │
│  │   847    │  │ R$ 84K   │  │  3.2%   │  │  +23     │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                          │
│  ┌──────────────────┐  ┌───────────────────────────┐    │
│  │ MRR Growth       │  │ Tenants por Plano          │    │
│  │   📈 (line chart) │  │   🍩 (donut chart)         │    │
│  └──────────────────┘  └───────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Agendamentos (últimos 30 dias)                    │   │
│  │ ████████████████████░░░░  📈                       │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Dashboard 2: Saúde Técnica (Operação)

```
┌─────────────────────────────────────────────────────────┐
│            BARBERSAAS — SAÚDE TÉCNICA                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Uptime   │  │ P95 Lat  │  │ Error    │  │ 4xx Rate │ │
│  │ 99.97%   │  │  180ms   │  │  0.02%   │  │  1.1%    │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                          │
│  ┌──────────────────┐  ┌───────────────────────────┐    │
│  │ Latência por EP  │  │ Throughput (req/s)         │    │
│  │   📊 (bar chart)  │  │   📈 (line chart)          │    │
│  └──────────────────┘  └───────────────────────────┘    │
│                                                          │
│  ┌──────────────────┐  ┌───────────────────────────┐    │
│  │ DB Connections   │  │ Redis Hit Rate             │    │
│  │   📈              │  │   📈 (target: >90%)        │    │
│  └──────────────────┘  └───────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Dashboard 3: Tenant (Por Empresa)

Acessível pelo admin do tenant em seu painel:
- Agendamentos do dia/semana/mês
- Taxa de ocupação
- Faturamento
- Cancelamentos
- Avaliações

---

## 14.6 Error Tracking (Sentry)

### O que vai para o Sentry

- Exceções não tratadas (500)
- Erros de integração (gateway, WhatsApp, e-mail)
- Erros de validação inesperados

### O que NÃO vai para o Sentry

- Erros 4xx (responsabilidade do cliente)
- Erros de rate limit
- Erros tratados com fallback

### Workflow

1. Erro ocorre em produção
2. Sentry captura stack trace + contexto (tenant_id, user_id, request_id)
3. Notificação no e-mail/telegram
4. Criação de issue automática
5. Resolução → marca como resolved
6. Regressão → reabre automaticamente

---

## 14.7 Ferramentas e Custos

| Ferramenta | Plano | Custo Mensal (Estimado) |
|-----------|-------|------------------------|
| Grafana Cloud (Metrics + Logs + Traces) | Free tier | R$ 0 (até 10K metrics, 50GB logs) |
| Prometheus | Self-hosted | R$ 0 (incluído na infra) |
| Loki | Self-hosted | R$ 0 (incluído na infra) |
| Tempo | Self-hosted | R$ 0 (incluído na infra) |
| Sentry | Free tier | R$ 0 (até 5K events/mês) |
| Cloudflare Analytics | Free | R$ 0 |

**Custo total de observabilidade (MVP): R$ 0.**  
**Custo em escala (10K tenants): ~R$ 500-1.000/mês (Grafana Cloud Pro).**

---

> **Princípio:** Observabilidade não é sobre ter dados — é sobre ter respostas. Quando um cliente reportar "meu agendamento sumiu", você deve ser capaz de rastrear exatamente o que aconteceu, em qual serviço, em qual momento, sem fazer ssh em servidor nenhum.
