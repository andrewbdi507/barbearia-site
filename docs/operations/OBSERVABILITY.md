# OBSERVABILITY.md — Observabilidade

## Stack

```
┌─────────────────────────────────────────────────────────┐
│                   OBSERVABILITY STACK                    │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│  │ METRICS  │   │  TRACES  │   │   LOGS   │            │
│  │Prometheus│   │OpenTelem.│   │  Loki    │            │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘            │
│       └──────────────┼──────────────┘                   │
│                 ┌────▼─────┐                             │
│                 │  Grafana  │ ← Dashboards + Alertas     │
│                 └──────────┘                             │
│                                                          │
│  + AlertManager (routing de alertas)                     │
│  + Node Exporter (métricas de host)                      │
│  + Promtail (shipper de logs)                            │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Logs (Loki + Promtail)

### Formato Estruturado

Todo log contém:
```json
{
  "timestamp": "2026-07-20T14:30:00.123Z",
  "level": "INFO",
  "module": "app.modules.scheduling.service",
  "event": "booking.created",
  "request_id": "req_abc123",
  "correlation_id": "corr_xyz789",
  "workspace_id": "ws_...",
  "user_id": "usr_...",
  "ip": "203.0.113.1",
  "duration_ms": 45.2,
  "error": null
}
```

### Níveis

| Nível | Uso |
|-------|-----|
| DEBUG | Detalhes de desenvolvimento |
| INFO | Eventos de negócio (booking.created, payment.paid) |
| WARNING | Degradações (cache miss, retry) |
| ERROR | Falhas tratadas (validação, timeout) |
| CRITICAL | Falhas não tratadas (exceptions) |

### Acesso

- **Grafana → Explore → Loki**: Pesquisa full-text nos logs
- **Query examples:**
  ```
  {service="backend", level="ERROR"} | json
  {container="barbershop-prod-backend"} |= "booking"
  {service="backend"} | json | duration_ms > 1000
  ```

---

## 2. Métricas (Prometheus + Grafana)

### Golden Signals

| Sinal | Métrica | Dashboard |
|-------|---------|-----------|
| **Latency** | `http_request_duration_seconds` (P50, P95, P99) | Operations → Response Time |
| **Traffic** | `http_requests_total` (rate) | Operations → Throughput |
| **Errors** | `http_requests_total{status=~"5.."}` | Operations → HTTP Status |
| **Saturation** | `process_cpu_seconds_total`, `process_resident_memory_bytes` | Operations → CPU/Memory |

### Métricas de Negócio

| Métrica | Descrição |
|---------|-----------|
| `bookings_created_total` | Agendamentos criados |
| `bookings_completed_total` | Agendamentos concluídos |
| `bookings_cancelled_total` | Cancelamentos |
| `bookings_no_show_total` | No-shows |
| `payments_total{status="paid"}` | Pagamentos aprovados |
| `payments_total{status="failed"}` | Pagamentos falhos |
| `new_customers_total` | Novos clientes |
| `revenue_total` | Receita total |

### Métricas de Infra

| Métrica | Fonte |
|---------|-------|
| CPU, Memory, Disk | Node Exporter (:9100) |
| PostgreSQL connections, locks | postgres_exporter (:9187) |
| Redis memory, keys, clients | redis_exporter (:9121) |

### Acesso

- **Grafana:** http://localhost:3000 (admin / senha do .env)
- **Prometheus:** http://localhost:9090 (query direta)
- **Dashboard principal:** "Barbershop SaaS — Operations"

---

## 3. Alertas (Prometheus AlertManager)

### Canais

| Canal | Uso |
|-------|-----|
| Slack | #alerts-barbershop |
| Email | platform@barbershop.com |
| PagerDuty (futuro) | On-call rotation |

### Regras

| Alerta | Severidade | Threshold |
|--------|:----------:|-----------|
| APIDown | CRITICAL | `up{job="backend"} == 0` por 1m |
| DatabaseDown | CRITICAL | `pg_up == 0` por 1m |
| RedisDown | CRITICAL | `redis_up == 0` por 1m |
| HighErrorRate | CRITICAL | 5xx > 5% por 5m |
| WorkerQueueStalled | CRITICAL | Sem processamento por 10m |
| HighCPUUsage | WARNING | CPU > 80% por 10m |
| HighMemory | WARNING | Mem > 1.5 GB por 10m |
| DiskSpaceLow | WARNING | < 20% livre |
| HighLatency | WARNING | P95 > 2s por 10m |
| HighNoShowRate | WARNING | > 30% por 30m |
| BackupFailed | WARNING | Último backup > 24h |

**Arquivo:** `config/prometheus/alerts.yml`

---

## 4. Health Checks

### Endpoints

| Endpoint | Tipo | Descrição |
|----------|------|-----------|
| `GET /health/live` | Liveness | App está rodando |
| `GET /health/ready` | Readiness | App pronta para tráfego (DB+Redis OK) |
| `GET /health` | Geral | Status completo |
| `GET /metrics` | Prometheus | Métricas no formato Prometheus |

### Exemplo de Resposta

```json
GET /health
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 345600,
  "checks": {
    "database": "ok",
    "redis": "ok",
    "migrations": "up_to_date"
  }
}
```

---

## 5. Tracing Distribuído (OpenTelemetry — Planejado)

Quando habilitado (`OTEL_EXPORTER_ENABLED=true`):
- Cada request gera um `trace_id` propagado via headers
- Spans: HTTP request → Service → Repository → DB query
- Visualização: Jaeger UI (http://localhost:16686)
- Sampling: 10% produção, 100% staging

---

## Dashboards

### Operational (`Barbershop SaaS — Operations`)
- KPIs: Success Rate, P95 Latency, RPS, Disk
- Gráficos: Throughput, Response Time, CPU, Memory
- Negócio: Bookings/hora, Payments/hora

### Business (planejado)
- Revenue Dashboard (por tenant, por período)
- Occupancy Dashboard (taxa de ocupação)
- Customer Dashboard (aquisição, retenção, churn)
