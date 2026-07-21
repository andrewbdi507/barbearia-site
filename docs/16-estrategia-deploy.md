# 16 — Estratégia de Deploy

---

## 16.1 Fase 0: MVP (Hoje — 0 a 500 tenants)

### Arquitetura de Deploy

```
┌─────────────────────────────────────────────────────────┐
│               VPS Única (Hostinger / DigitalOcean)       │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Docker Compose                       │   │
│  │                                                   │   │
│  │  ┌─────────┐  ┌─────────┐  ┌──────────────────┐  │   │
│  │  │ Next.js │  │ FastAPI │  │ FastAPI (Admin)  │  │   │
│  │  │ :3000   │  │ :8000   │  │ :8001            │  │   │
│  │  └─────────┘  └─────────┘  └──────────────────┘  │   │
│  │                                                   │   │
│  │  ┌──────────┐  ┌────────┐  ┌──────────────────┐  │   │
│  │  │PostgreSQL│  │ Redis  │  │ Nginx (reverse   │  │   │
│  │  │ :5432    │  │ :6379  │  │ proxy + SSL)     │  │   │
│  │  └──────────┘  └────────┘  └──────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

CDN: Cloudflare Free (DDoS, cache, SSL)
Backups: Script cron → S3/R2
CI/CD: GitHub Actions (build + deploy via SSH)
```

### Detalhes

| Aspecto | Decisão |
|---------|---------|
| **Servidor** | VPS Linux 4 vCPU, 8 GB RAM (~R$ 200/mês) |
| **Orquestração** | Docker Compose (simples, 1 arquivo) |
| **CI/CD** | GitHub Actions: build imagem → push registry → SSH deploy |
| **SSL** | Cloudflare (edge) + Let's Encrypt (origin) |
| **Domínio** | Cloudflare DNS |
| **Deploy** | Blue-green com Docker (stop old → start new, ~10s downtime) |
| **Rollback** | Reverter imagem Docker anterior |
| **Arquivos estáticos** | Servidos pelo Next.js, cacheados no Cloudflare |

### Vantagens
- Simplicidade máxima (1 dev gerencia tudo)
- Custo previsível e baixo
- Sem complexidade de Kubernetes

### Limitações
- Sem alta disponibilidade (single point of failure)
- Escalabilidade vertical apenas (upgrade de VPS)
- Downtime durante deploy (10s)
- Sem isolamento de recursos entre serviços

---

## 16.2 Fase 1: Crescimento (6 meses — 500 a 5.000 tenants)

### Arquitetura de Deploy

```
┌─────────────────────────────────────────────────────────┐
│              Kubernetes (Managed — DigitalOcean K8s)     │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │   Node Pool 1    │  │   Node Pool 2    │             │
│  │   (General)      │  │   (Memory Opt.)  │             │
│  │                   │  │                   │             │
│  │  ┌──────┐┌──────┐│  │  ┌──────┐┌──────┐│             │
│  │  │Next.js││ API  ││  │  │  DB  ││Redis ││             │
│  │  │  x2  ││  x3  ││  │  │  x2  ││  x3  ││             │
│  │  └──────┘└──────┘│  │  └──────┘└──────┘│             │
│  └──────────────────┘  └──────────────────┘             │
│                                                          │
│  Services:                                               │
│  • Horizontal Pod Autoscaler (CPU > 70%)                 │
│  • Ingress Controller (NGINX)                            │
│  • Cert-Manager (SSL automático)                         │
│  • External Secrets Operator                             │
│  • Persistent Volumes (DB, Redis)                        │
└─────────────────────────────────────────────────────────┘

Banco Gerenciado: DigitalOcean Managed PostgreSQL + Redis
CDN: Cloudflare Pro (R$ 80/mês)
CI/CD: GitHub Actions + Helm
```

### Evoluções

| Aspecto | Mudança |
|---------|---------|
| **Orquestração** | Docker Compose → Kubernetes (managed) |
| **Banco** | Container → Managed PostgreSQL (backups automáticos, read replicas) |
| **Cache** | Container → Managed Redis (failover automático) |
| **Deploy** | Blue-green → Rolling updates (zero downtime) |
| **Escala** | Vertical → Horizontal (HPA) |
| **SSL** | Cert-Manager (automático) |
| **Segredos** | .env → Kubernetes Secrets + External Secrets |
| **Monitoramento** | Prometheus + Grafana (dentro do cluster) |

### Custos Estimados

| Recurso | Custo Mensal |
|---------|:-----------:|
| K8s Cluster (2 nodes) | ~R$ 600 |
| Managed PostgreSQL (2 GB) | ~R$ 300 |
| Managed Redis (1 GB) | ~R$ 150 |
| Cloudflare Pro | R$ 80 |
| S3/R2 Storage | R$ 50 |
| **Total** | **~R$ 1.200** |

---

## 16.3 Fase 2: Escala (2 anos — 5.000 a 50.000+ tenants)

### Arquitetura de Deploy

```
┌─────────────────────────────────────────────────────────┐
│              Cloud Provider (AWS / GCP)                   │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │   Região: SP     │  │  Região: VA (DR) │             │
│  │                   │  │                   │             │
│  │  ┌────────────┐  │  │  ┌────────────┐  │             │
│  │  │ EKS / GKE  │  │  │  │ EKS / GKE  │  │             │
│  │  │ (K8s)      │  │  │  │ (standby)  │  │             │
│  │  └────────────┘  │  │  └────────────┘  │             │
│  │                   │  │                   │             │
│  │  ┌────────────┐  │  │                   │             │
│  │  │ RDS         │  │  │  Read Replica    │             │
│  │  │ PostgreSQL  │──┼──│  (cross-region)  │             │
│  │  │ (Multi-AZ)  │  │  │                   │             │
│  │  └────────────┘  │  │                   │             │
│  │                   │  │                   │             │
│  │  ┌────────────┐  │  │                   │             │
│  │  │ElastiCache  │  │  │                   │             │
│  │  │ Redis       │  │  │                   │             │
│  │  │ (Cluster)   │  │  │                   │             │
│  │  └────────────┘  │  │                   │             │
│  └──────────────────┘  └──────────────────┘             │
│                                                          │
│  S3 + CloudFront CDN (global)                            │
│  WAF + Shield (DDoS)                                     │
│  Route 53 (DNS)                                          │
└─────────────────────────────────────────────────────────┘
```

### Evoluções

| Aspecto | Mudança |
|---------|---------|
| **Cloud** | DigitalOcean → AWS/GCP (mais serviços gerenciados) |
| **Banco** | Single → Multi-AZ com read replicas |
| **Cache** | Single → Redis Cluster (sharding) |
| **CDN** | Cloudflare → CloudFront (integração nativa AWS) |
| **Disaster Recovery** | Região secundária com replicação |
| **Segurança** | WAF, Shield Advanced, GuardDuty |
| **CI/CD** | GitHub Actions → GitHub Actions + ArgoCD (GitOps) |

### Custos Estimados

| Recurso | Custo Mensal |
|---------|:-----------:|
| EKS Cluster | ~R$ 800 |
| RDS PostgreSQL (Multi-AZ, 16 GB) | ~R$ 2.500 |
| ElastiCache Redis Cluster | ~R$ 1.500 |
| CloudFront + S3 | ~R$ 500 |
| WAF + Shield | ~R$ 300 |
| Observabilidade | ~R$ 1.000 |
| **Total** | **~R$ 6.600** |

---

## 16.4 Pipeline de CI/CD

### GitHub Actions Workflow (Todas as Fases)

```
Push to main / PR
    │
    ▼
┌─────────────────────────────┐
│ 1. Lint & Type Check        │
│    • ruff (Python)          │
│    • eslint (JS/TS)         │
│    • mypy / pyright         │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 2. Test                     │
│    • Unit tests (pytest)    │
│    • Integration tests      │
│    • Coverage ≥ 80%         │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 3. Security Scan            │
│    • bandit (Python SAST)   │
│    • npm audit              │
│    • trivy (container scan) │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 4. Build                    │
│    • Docker build           │
│    • Tag: git sha + branch  │
│    • Push to registry       │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 5. Deploy (Staging)         │
│    • Auto (on main push)    │
│    • Smoke tests            │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 6. Deploy (Production)      │
│    • Manual approval        │
│    • Rolling update /       │
│      Blue-green             │
│    • Health check           │
│    • Auto-rollback on fail  │
└─────────────────────────────┘
```

---

## 16.5 Estratégia de Branching

```
main ──────────────────────────────► (production)
  │
  ├── feature/xxx ──► PR ──► main
  │
  ├── fix/xxx ──────► PR ──► main
  │
  └── release/v1.x (tag)
```

- **main**: sempre deployável
- **feature/**: branches de curta duração (< 3 dias)
- **PR obrigatório** para merge
- **Squash merge** (histórico limpo)
- **Tag semver** no release: `v1.2.3`

---

## 16.6 Estratégia de Rollback

| Cenário | Como reverter |
|---------|--------------|
| **Código** | `kubectl rollout undo deployment/api` (K8s) ou `docker-compose up -d` com imagem anterior |
| **Banco de dados** | Migration rollback automática (se definida) ou restore de backup |
| **Configuração** | Reverter PR de infra-as-code (Terraform/Pulumi) |
| **Desastre total** | Restore completo via procedimento de disaster recovery |

---

> **Princípio:** O deploy deve ser um evento sem drama. Comece simples (VPS + Docker Compose), evolua para Kubernetes apenas quando a complexidade adicional se justificar. Uma VPS bem configurada leva você até 500 tenants sem problemas. Não complique antes da hora.
