# INFRASTRUCTURE.md — Arquitetura de Infraestrutura

## Visão Geral

A plataforma Barbershop SaaS segue uma arquitetura modular em camadas, preparada para evoluir de VPS única → Docker Swarm → Kubernetes sem reescrita.

```
┌──────────────────────────────────────────────────────────────────┐
│                         CLOUDFLARE                               │
│               CDN • DDoS Protection • SSL (Edge)                 │
└───────────────────────────┬──────────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│                     LOAD BALANCER / NGINX                        │
│          Reverse Proxy • SSL Termination • Rate Limiting         │
│          Security Headers • Static Files • Gzip                  │
└──┬──────────────┬──────────────┬──────────────┬──────────────────┘
   │              │              │              │
   ▼              ▼              ▼              ▼
┌──────┐   ┌──────────┐  ┌──────────┐  ┌──────────────┐
│ API  │   │  Worker  │  │Scheduler │  │  Prometheus   │
│ x2-4 │   │   x2     │  │   x1     │  │  + Grafana    │
│:8000 │   │          │  │          │  │  + Loki       │
└──┬───┘   └────┬─────┘  └────┬─────┘  └──────────────┘
   │            │              │
   ▼            ▼              ▼
┌──────────────────────────────────────┐
│              REDIS 7                  │
│    Cache • Queue • Rate Limiting      │
│    Sessions • Feature Flags           │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│          POSTGRESQL 16               │
│    Primary DB • RLS • WAL Archiving  │
│    Materialized Views • Extensions   │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│        OBJECT STORAGE (S3/R2)        │
│    Uploads • Backups • Static Media   │
└──────────────────────────────────────┘
```

---

## Componentes

### 1. Nginx (Reverse Proxy)

| Função | Configuração |
|--------|-------------|
| SSL Termination | Let's Encrypt + Cloudflare |
| Static Files | Admin SPA + Public Site |
| Rate Limiting | API: 100r/s, Auth: 5r/m |
| Security Headers | HSTS, CSP, X-Frame-Options, XSS, Referrer-Policy |
| Proxy | `/api/*` → backend:8000 |
| Health Check | `/health` → 200 OK |

**Arquivo:** `docker/nginx/default.conf`

### 2. Backend API (FastAPI + Uvicorn)

| Aspecto | Dev | Staging | Production |
|---------|-----|---------|------------|
| Workers | 1 (reload) | 2 | 4 |
| Loop | asyncio | uvloop | uvloop |
| HTTP parser | h11 | httptools | httptools |
| Memory limit | — | 1 GB | 2 GB |
| CPU limit | — | 1.0 | 2.0 |
| Replicas | 1 | 1 | 2 |

### 3. Worker (Background Jobs)

Processa notificações, exportações, processamento de imagens.
- **Queue:** Redis list
- **Retry:** Exponential backoff (1m → 5m → 15m → 1h → 6h → DLQ)
- **Concorrência:** 10 jobs simultâneos

### 4. Scheduler (Cron)

Tarefas agendadas:
- Agregação de analytics (a cada hora)
- Limpeza de sessões expiradas (diário)
- Disparo de backup (diário às 2h)
- Expiração de coupons (diário)
- Envio de lembretes de agendamento (a cada 15min)

### 5. PostgreSQL 16

| Configuração | Valor |
|-------------|-------|
| Pool Size | 20 |
| Max Overflow | 10 |
| RLS | Por tenant |
| WAL Level | replica |
| Extensions | uuid-ossp, pgcrypto, citext |
| Backup | pg_dump (custom) + WAL archiving |

### 6. Redis 7

| Configuração | Valor |
|-------------|-------|
| Max Memory | 1 GB (prod) |
| Eviction | allkeys-lru |
| Persistence | AOF + RDB |
| DB 0 | Cache (tenant, branding, settings) |
| DB 1 | Queue (worker jobs) |
| DB 2 | Rate Limiting |
| Senha | Obrigatória |

---

## Network

Todas as comunicações internas são via rede Docker bridge `barbershop-{env}-net`.
Apenas Nginx expõe portas 80/443 publicamente.
PostgreSQL e Redis só aceitam conexões de localhost (127.0.0.1).

---

## Storage (Objetos)

| Provider | Config | Uso |
|----------|--------|-----|
| Local | `STORAGE_PROVIDER=local` | Desenvolvimento |
| AWS S3 | `STORAGE_PROVIDER=s3` | Produção (AWS) |
| Cloudflare R2 | `STORAGE_PROVIDER=r2` | Produção (CF) |
| Azure Blob | `STORAGE_PROVIDER=azure` | Produção (Azure) |
| GCS | `STORAGE_PROVIDER=gcs` | Produção (GCP) |

Troca via variável de ambiente `STORAGE_PROVIDER` — sem alteração de código.

---

## Path de Evolução

```
Fase 0 (MVP)          Fase 1 (Crescimento)     Fase 2 (Enterprise)
─────────────────     ────────────────────     ───────────────────
VPS Única             Docker Swarm              Kubernetes (EKS/GKE)
Docker Compose        Multi-node                Auto-scaling
1 instância/postgres  PostgreSQL RDS            Multi-region
                       Redis ElastiCache         Service Mesh (Istio)
                       S3/R2 para uploads        GitOps (ArgoCD)
```

---

## Capacity Planning

| Métrica | 500 tenants | 2.000 tenants | 10.000+ tenants |
|---------|:-----------:|:-------------:|:---------------:|
| API replicas | 2 | 4 | 8+ (auto-scale) |
| DB size | ~5 GB | ~20 GB | ~100+ GB |
| Redis memory | 1 GB | 2 GB | 4 GB |
| Storage | 50 GB | 200 GB | 1 TB+ |
| Bandwidth | 100 Mbps | 500 Mbps | 1 Gbps+ |
| VPS | 4 vCPU, 8 GB | 8 vCPU, 16 GB | Kubernetes |
