# 03 — Scalability Review

> Análise de escalabilidade do sistema de 10 a 100.000 tenants.  
> O que quebra primeiro em cada patamar e como evoluir.

---

## 1. Visão Geral da Escalabilidade

```
         10        100       1.000      10.000     100.000
         ├─────────┼─────────┼──────────┼──────────┼──────────►

VPS      ████████░░
Simples  ████████░░
         ████████░░

K8s               ████████████████████████░░
Managed           ████████████████████████░░
                   ████████████████████████░░

AWS/GCP                             ██████████████████████████████
Multi-AZ                            ██████████████████████████████
                                    ██████████████████████████████

Sharding                                           ██████████████████
Global                                             ██████████████████
```

---

## 2. Análise por Componente

### 2.1 PostgreSQL

| Patamar | Configuração | Gargalo | Solução |
|---------|-------------|---------|---------|
| **10-100** tenants | VPS compartilhada (4-8 GB) | Nenhum | — |
| **100-500** | Managed PostgreSQL (8 GB) | Conexões simultâneas | PgBouncer |
| **500-1.000** | + 1 read replica | Write throughput | Otimização de queries |
| **1.000-5.000** | + 2-3 read replicas | Tamanho do dataset | Particionamento (bookings, audit_logs) |
| **5.000-10.000** | Multi-AZ, 32 GB | Write throughput | Sharding por faixa de tenant_id |
| **10.000-50.000** | Sharding horizontal | Complexidade operacional | Equipe DBA dedicada |
| **50.000+** | Vitess / Citus | Orquestração de shards | Múltiplos clusters |

**Quando migrar:** O PostgreSQL aguenta ~5.000 tenants ativos em schema compartilhado com índices adequados. A partir de ~50.000, considere sharding.

### 2.2 Redis

| Patamar | Configuração | Gargalo | Solução |
|---------|-------------|---------|---------|
| **10-500** tenants | Single instance (1 GB) | Nenhum | — |
| **500-1.000** | Managed Redis (2 GB) | Memória | Aumentar instância |
| **1.000-5.000** | Redis Cluster (sharding) | Conexões | Cluster mode |
| **5.000+** | ElastiCache / MemoryDB | — | Gerenciado pela AWS |

### 2.3 API (FastAPI)

| Patamar | Configuração | Gargalo | Solução |
|---------|-------------|---------|---------|
| **10-500** tenants | 1-2 workers (VPS) | Nenhum | — |
| **500-1.000** | 4 workers (K8s, 2 pods) | CPU | HPA (horizontal auto-scaling) |
| **1.000-5.000** | 8+ workers (K8s, 4 pods) | — | Auto-scaling |
| **5.000+** | Auto-scaling cluster | — | — |

### 2.4 Frontend (Next.js / React)

| Patamar | Configuração | Gargalo | Solução |
|---------|-------------|---------|---------|
| **10-1.000** tenants | CDN (Cloudflare) | Nenhum | Cache agressivo |
| **1.000-10.000** | CDN + SSR | Tempo de build (se SSR) | ISR (Incremental Static Regeneration) |
| **10.000+** | CDN multi-region | Latência em regiões distantes | Cloudflare Argo / AWS Global Accelerator |

### 2.5 Storage (S3 / R2)

| Patamar | Configuração | Gargalo | Solução |
|---------|-------------|---------|---------|
| **10-1.000** tenants | R2 (S3-compatible) | Nenhum (escala infinita) | — |
| **1.000-10.000** | S3 + CloudFront | Custo de egress | R2 (zero egress fees) |
| **10.000+** | S3 multi-region | Latência | Replicação cross-region |

---

## 3. O Que Quebra Primeiro

### Patamar 1: ~100 tenants — Conexões de Banco
**Sintoma:** Erros "too many connections" no PostgreSQL.  
**Causa:** Cada worker da API abre conexões. Sem PgBouncer, o pool esgota.  
**Solução:** Configurar PgBouncer (transaction pooling).  
**Custo:** ~R$ 0 (software livre, mesmo servidor).

### Patamar 2: ~500 tenants — Grid de Horários
**Sintoma:** Latência elevada ao carregar slots disponíveis (> 500ms).  
**Causa:** Consulta de disponibilidade é computacionalmente cara. Sem cache, cada request recalcula.  
**Solução:** Cache Redis (30s TTL) + pré-computação de slots.  
**Custo:** ~R$ 0 (já usa Redis).

### Patamar 3: ~1.000 tenants — Write Throughput no Banco
**Sintoma:** Agendamentos concorrentes causam locks e timeouts.  
**Causa:** Todos os writes vão para o primary. Read replicas não ajudam em write.  
**Solução:** Otimizar índices + particionar tabela bookings por mês.  
**Custo:** Tempo de desenvolvimento (~1 semana).

### Patamar 4: ~5.000 tenants — Tamanho do Dataset
**Sintoma:** Vacuum lento, backups demorados, queries de relatório pesadas.  
**Causa:** Milhões de registros em bookings (5K tenants × 20 bookings/dia × 365 dias = 36M/ano).  
**Solução:** Particionamento + arquivamento (bookings > 2 anos → cold storage).  
**Custo:** ~R$ 200/mês (storage adicional).

### Patamar 5: ~50.000 tenants — Sharding
**Sintoma:** PostgreSQL atinge limite de capacidade em schema único.  
**Causa:** Índices, vacuum, e backups se tornam inviáveis em tabela única.  
**Solução:** Sharding por faixa de tenant_id ou migração para schema por tenant.  
**Custo:** ~R$ 5.000+/mês + equipe DBA.

---

## 4. Estratégia de Cache por Patamar

| Patamar | Estratégia |
|---------|-----------|
| **MVP** | Cache de slots (Redis, 30s TTL) + cache de página (Cloudflare, 5 min) |
| **500** | Cache de dados do tenant (Redis, 5 min) + cache de query (Redis) |
| **1.000** | Materialized views para dashboards (refresh a cada 5 min) |
| **5.000** | CDN multi-region + Redis Cluster |
| **10.000+** | Edge computing (Cloudflare Workers) para personalização de cache por tenant |

---

## 5. Custos de Infraestrutura por Patamar (Revisão)

| Patamar | Tenants | Custo Mensal | Custo/Tenant | % Receita (est.) |
|---------|:-------:|:------------:|:------------:|:----------------:|
| MVP | 10 | R$ 206 | R$ 20,60 | — (beta) |
| V1 | 200 | R$ 1.000 | R$ 5,00 | ~5% |
| V2 | 1.000 | R$ 5.500 | R$ 5,50 | ~5% |
| V3 | 5.000 | R$ 19.500 | R$ 3,90 | ~3% |
| V4 | 10.000 | R$ 37.400 | R$ 3,74 | ~3% |

---

## 6. Testes de Carga Recomendados

| Patamar | Teste | Ferramenta |
|---------|-------|-----------|
| **MVP** | 50 agendamentos simultâneos | Locust / k6 |
| **V1** | 200 agendamentos simultâneos + 1.000 leituras/min | k6 |
| **V2** | 500 agendamentos simultâneos + 5.000 leituras/min | k6 + distributed |
| **V3** | 2.000 agendamentos simultâneos | k6 cloud |

---

> **Nota Final (Escalabilidade): 7.5/10** — A arquitetura está preparada para escalar de 10 a 10.000 tenants com evoluções incrementais bem documentadas. Os gargalos estão identificados e as soluções são conhecidas. O risco é a transição entre patamares — especialmente schema único → sharding — que exigirá planejamento cuidadoso com meses de antecedência.
