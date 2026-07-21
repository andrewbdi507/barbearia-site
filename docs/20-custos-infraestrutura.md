# 20 — Custos de Infraestrutura

---

## 20.1 Premissas

- Stack: PostgreSQL, Redis, API (FastAPI), Frontend (Next.js + React), S3 Storage, CDN
- As estimativas são para AWS (São Paulo), mas os preços são similares em DigitalOcean, GCP ou Azure
- Custos em reais (R$), considerando USD 1 = R$ 5,00 (aproximado)
- Custos de ferramentas SaaS (Sentry, Grafana Cloud) são adicionais
- Os valores dependem do provedor escolhido e do volume real de uso; estas são estimativas qualitativas de referência

---

## 20.2 Cenário 1: 10 Clientes (MVP)

| Componente | Especificação | Custo Mensal (R$) |
|------------|:------------:|:-----------------:|
| **Computação** | VPS 4 vCPU, 8 GB RAM (Hostinger/DO) | 200 |
| **Banco de Dados** | PostgreSQL (mesma VPS) | 0 (incluído) |
| **Cache** | Redis (mesma VPS) | 0 (incluído) |
| **Storage (S3/R2)** | Cloudflare R2 (10 GB) | 0 (free) |
| **CDN** | Cloudflare Free | 0 |
| **Domínio** | Registro .com.br | 4 |
| **E-mail Transacional** | Resend / SendGrid Free (100/dia) | 0 |
| **Monitoramento** | Grafana Cloud Free / Sentry Free | 0 |
| **Backup** | S3/R2 storage | 2 |
| **Total** | | **~R$ 206** |

**Custo por tenant:** ~R$ 20,60  
**Custo aceitável até:** R$ 500/mês  
**Folga:** ~59%

---

## 20.3 Cenário 2: 100 Clientes

| Componente | Especificação | Custo Mensal (R$) |
|------------|:------------:|:-----------------:|
| **Computação** | VPS 8 vCPU, 16 GB RAM | 400 |
| **Banco de Dados** | Managed PostgreSQL 2 GB (DigitalOcean) | 300 |
| **Cache** | Managed Redis 1 GB (DigitalOcean) | 150 |
| **Storage (S3/R2)** | Cloudflare R2 (50 GB) | 10 |
| **CDN** | Cloudflare Free/Pro | 0–80 |
| **Domínios** | Plataforma + tenants | 50 |
| **E-mail Transacional** | AWS SES (~10K e-mails/mês) | 5 |
| **WhatsApp API** | Evolution API (self-hosted) + Meta costs | 50 |
| **Monitoramento** | Grafana Cloud / Sentry (dev) | 0 |
| **Backup** | S3/R2 storage | 15 |
| **Total** | | **~R$ 980–1.060** |

**Custo por tenant:** ~R$ 10,00  
**Custo aceitável até:** R$ 1.500/mês  
**Folga:** ~30%

### O que provavelmente precisará evoluir
- Banco de dados migra para serviço gerenciado (backups automáticos, maior confiabilidade)
- Redis em serviço gerenciado (evitar perda de sessões/cache)
- WhatsApp API exigirá conta Business verificada na Meta

---

## 20.4 Cenário 3: 500 Clientes

| Componente | Especificação | Custo Mensal (R$) |
|------------|:------------:|:-----------------:|
| **Orquestração** | Kubernetes (DO K8s, 2 nodes × 4 vCPU) | 600 |
| **Banco de Dados** | Managed PostgreSQL 8 GB + read replica | 800 |
| **Cache** | Managed Redis 2 GB | 250 |
| **Storage (S3/R2)** | R2 200 GB | 40 |
| **CDN** | Cloudflare Pro | 80 |
| **Domínios** | Plataforma + tenants | 100 |
| **E-mail Transacional** | AWS SES (~50K e-mails/mês) | 25 |
| **WhatsApp API** | Meta Business API | 150 |
| **Monitoramento** | Grafana Cloud (Pro) + Sentry (Team) | 300 |
| **Backup** | S3/R2 storage | 50 |
| **Load Balancer** | Kubernetes native / DO LB | 50 |
| **Total** | | **~R$ 2.445** |

**Custo por tenant:** ~R$ 4,89  
**Custo aceitável até:** R$ 4.000/mês  
**Folga:** ~39%

### O que provavelmente precisará evoluir
- Migração para Kubernetes (gerenciamento de múltiplos serviços)
- Read replica no banco (separar leitura do site público da escrita do admin)
- Monitoramento mais robusto (Grafana Cloud Pro para retenção maior)
- CDN Pro para regras de cache mais granulares

---

## 20.5 Cenário 4: 1.000 Clientes

| Componente | Especificação | Custo Mensal (R$) |
|------------|:------------:|:-----------------:|
| **Orquestração** | Kubernetes (3 nodes × 8 vCPU) | 1.200 |
| **Banco de Dados** | RDS PostgreSQL 16 GB + 2 read replicas | 2.000 |
| **Cache** | ElastiCache Redis 4 GB (cluster mode) | 600 |
| **Storage (S3)** | S3 Standard 500 GB | 100 |
| **CDN** | CloudFront + Cloudflare Pro | 300 |
| **Domínios** | Plataforma + tenants | 200 |
| **E-mail Transacional** | AWS SES (~100K e-mails/mês) | 50 |
| **WhatsApp API** | Meta Business API | 300 |
| **Monitoramento** | Grafana Cloud Pro + Sentry Business | 500 |
| **Backup** | S3 + Glacier | 150 |
| **WAF** | AWS WAF | 150 |
| **Total** | | **~R$ 5.550** |

**Custo por tenant:** ~R$ 5,55  
**Custo aceitável até:** R$ 8.000/mês  
**Folga:** ~30%

### O que provavelmente precisará evoluir
- Migração para AWS/GCP (mais opções de serviços gerenciados)
- Múltiplas read replicas (aumento de tráfego de leitura)
- WAF dedicado (proteção contra ataques)
- Redis cluster mode para maior capacidade de cache

---

## 20.6 Cenário 5: 5.000 Clientes

| Componente | Especificação | Custo Mensal (R$) |
|------------|:------------:|:-----------------:|
| **Orquestração** | EKS/GKE (6+ nodes, auto-scaling) | 3.500 |
| **Banco de Dados** | RDS Multi-AZ 32 GB + 3 replicas | 5.000 |
| **Cache** | ElastiCache Redis 16 GB (cluster) | 2.000 |
| **Storage (S3)** | S3 2 TB + CloudFront | 500 |
| **CDN** | CloudFront + Shield Standard | 800 |
| **Domínios** | Plataforma + tenants | 500 |
| **E-mail Transacional** | AWS SES (~500K/mês) | 200 |
| **WhatsApp API** | Meta Business API (volume) | 1.000 |
| **SMS** | Zenvia/Twilio (~100K/mês) | 1.000 |
| **Monitoramento** | Grafana Cloud + Sentry + Datadog | 2.000 |
| **Backup** | S3 + Glacier + Cross-region | 500 |
| **WAF + Shield** | AWS Shield Advanced | 2.000 |
| **Suporte** | Intercom / Zendesk | 500 |
| **Total** | | **~R$ 19.500** |

**Custo por tenant:** ~R$ 3,90  
**Custo aceitável até:** R$ 50.000/mês (10% da receita)  
**Folga:** ~61%

### O que provavelmente precisará evoluir
- Infraestrutura multi-AZ para alta disponibilidade
- Shield Advanced para proteção DDoS (alvo maior)
- Ferramentas de suporte profissional
- Equipe de operações (fim do "1 dev faz tudo")

---

## 20.7 Cenário 6: 10.000 Clientes

| Componente | Especificação | Custo Mensal (R$) |
|------------|:------------:|:-----------------:|
| **Orquestração** | EKS/GKE (12+ nodes, auto-scaling) | 6.000 |
| **Banco de Dados** | RDS Multi-AZ 64 GB + 4 replicas | 10.000 |
| **Cache** | ElastiCache Redis 32 GB (cluster) | 4.000 |
| **Storage** | S3 5 TB + CloudFront | 1.200 |
| **CDN** | CloudFront Global | 1.500 |
| **Domínios** | + SSL automation | 800 |
| **E-mail** | SES (~1M/mês) | 400 |
| **WhatsApp** | Meta API (alto volume) | 2.500 |
| **SMS** | Zenvia/Twilio (~200K/mês) | 2.000 |
| **Observabilidade** | Grafana + Sentry + Datadog | 3.000 |
| **Backup** | Multi-region, Glacier | 1.000 |
| **Segurança** | WAF + Shield + GuardDuty | 3.500 |
| **Suporte** | Plataforma de suporte | 1.500 |
| **Total** | | **~R$ 37.400** |

**Custo por tenant:** ~R$ 3,74  
**Custo aceitável até:** R$ 100.000/mês (8% da receita)  
**Folga:** ~63%

### O que provavelmente precisará evoluir
- Arquitetura multi-region (América Latina)
- Sharding de banco de dados (ou separação de tenants enterprise)
- Equipe DevOps dedicada
- SOC/NOC para operação 24/7

---

## 20.8 Gráfico de Economia de Escala

```
Custo por Tenant (R$)
    │
 20 │ ●
    │
 15 │
    │
 10 │   ●
    │
  5 │       ●     ●     ●      ●      ●
    │
  0 └─────┬─────┬─────┬──────┬──────┬──────
        10    100   500   1.000  5.000  10.000
                      Tenants
```

O custo por tenant cai significativamente com a escala, comprovando o modelo SaaS.

---

## 20.9 Recomendações de Otimização de Custos

1. **Use free tiers ao máximo no início** (Cloudflare, Sentry, Grafana Cloud, GitHub Actions)
2. **Reserve instâncias** (AWS Reserved / Savings Plans) para 30–40% de desconto a partir de 500 tenants
3. **Cache agressivo** reduz carga no banco (maior custo)
4. **Mova logs frios para Glacier** após 30 dias
5. **Compartilhe infraestrutura entre tenants** (nosso modelo já faz isso)
6. **Monitore custos diariamente** — uma instância esquecida pode custar caro
7. **Negocie com provedores** quando atingir escala (1.000+ tenants)

---

> **Princípio:** Infraestrutura é um investimento, não um custo. O objetivo não é gastar zero — é gastar proporcionalmente à receita. Com 10.000 tenants pagando em média R$ 120/mês, a receita é de R$ 1,2M/mês e a infra representa ~3% disso. Este é um negócio saudável.
