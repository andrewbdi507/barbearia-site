# RELATÓRIO DE ESCALABILIDADE — Auditoria Final

## 1. Capacity Analysis

### 1.1 Quantos clientes suporta?

| Configuração | Tenants | Usuários | Bookings/dia | Infra |
|-------------|:-------:|:--------:|:------------:|-------|
| **Atual (VPS 4 vCPU, 8 GB)** | 500 | 5.000 | 10.000 | Docker Compose |
| **Otimizado (+ cache + mat views)** | 1.000 | 10.000 | 20.000 | Docker Compose + PgBouncer |
| **Escalado (Swarm 3 nós)** | 2.000 | 20.000 | 50.000 | Docker Swarm + RDS |
| **Enterprise (K8s)** | 10.000+ | 100.000+ | 250.000+ | Kubernetes + Multi-AZ |

### 1.2 Quantos agendamentos simultâneos?

| Cenário | Capacidade |
|---------|:----------:|
| Pico de abertura (1 min) | ~500 bookings |
| Horário comercial (sustentado) | ~200 bookings/min |
| Disponibilidade (consulta) | ~5000 consultas/min |

---

## 2. Gargalos por Escala

### 100 Empresas
- **Gargalo:** Nenhum. VPS 4 vCPU/8GB confortável.
- **Ação:** Monitorar. Backups diários ok.

### 1.000 Empresas
- **Gargalo:** Analytics KPIs recalculados. Customer 360° com múltiplos JOINs.
- **Ação:** Materialized views + Redis cache para perfis. PgBouncer.

### 10.000 Empresas
- **Gargalo:** PostgreSQL single instance. Uploads locais. Redis single instance.
- **Ação:** Migrar para RDS Multi-AZ + Read Replicas. S3/R2 para uploads. Redis Cluster.

### 100.000 Empresas
- **Gargalo:** Tudo single-region. Latência para usuários distantes. Escala manual.
- **Ação:** Kubernetes multi-region. CDN global. Database sharding por região. Event sourcing com Kafka.

---

## 3. Plano de Escala

```
Fase 0 (MVP)           Fase 1 (Crescimento)      Fase 2 (Enterprise)
──────────────────     ─────────────────────     ───────────────────
VPS única              Docker Swarm 3 nós         Kubernetes (EKS/GKE)
API: 2 replicas        API: 4-6 replicas          API: auto-scale HPA
PostgreSQL local       PostgreSQL RDS             RDS Multi-AZ + Read
Redis local            Redis ElastiCache          Redis Cluster
Uploads: disco local   Uploads: S3/R2             S3 + CloudFront CDN
Monitor: Prom+VPS      Monitor: managed Grafana   DataDog/NewRelic
CI/CD: GitHub Actions  CI/CD: +canary deploys     GitOps (ArgoCD)
```

---

## 4. Recomendações Imediatas (Pre-Go Live)

| Ação | Por quê |
|------|---------|
| Definir resource limits em todos os containers | Evitar que um container consuma tudo |
| Configurar auto-restart (`unless-stopped`) | Resiliência básica |
| Monitorar disco, RAM, CPU desde o dia 1 | Baseline para escala |
| Configurar alertas de capacidade (80% threshold) | Saber quando escalar |

---

## 5. Nota de Escalabilidade: **8.0 / 10**

**Justificativa:** A arquitetura é modular e preparada para evolução (VPS → Swarm → K8s). A separação em serviços independentes (API, Worker, Scheduler) permite escala granular. O principal limitador é o PostgreSQL single instance — adequado para até ~1000 tenants sem otimização adicional. O plano de evolução está documentado e não requer reescrita de código.

**Limite seguro atual:** 500 tenants com folga. 1000 tenants com otimizações leves.
