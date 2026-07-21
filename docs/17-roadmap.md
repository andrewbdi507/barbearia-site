# 17 — Roadmap

---

## 17.1 Visão Geral

```
MVP (Mês 0-3)        V1 (Mês 3-9)        V2 (Mês 9-18)       V3 (Mês 18-36)      V4 (Mês 36-60)
───────────────      ─────────────        ──────────────       ───────────────      ──────────────

Barbearias           + Salões             + Clínicas           + Qualquer           Expansão
10 beta              + Estúdios           + Psicólogos          negócio de           Internacional
                     50-200 tenants       + Dentistas           agendamento          + AI
                                         200-1.000 tenants     1.000-5.000          5.000-10.000+
```

---

## 17.2 MVP — Versão 0 (Mês 0–3)

### Objetivo: Validar o core com 10 barbearias beta.

### Funcionalidades

| Módulo | Entregas |
|--------|----------|
| **Tenant** | Cadastro, subdomínio automático, configuração básica |
| **Site Público** | Página inicial (logo, banner, cores), listagem de serviços, listagem de equipe |
| **Agendamento** | Profissional → Serviço → Horário, sem pagamento |
| **Painel Admin** | CRUD serviços, CRUD profissionais, agenda visual, configuração de horários |
| **Auth** | Login/senha, recuperação de senha, RBAC básico (admin + barber) |
| **Notificações** | WhatsApp (confirmação + lembrete 24h) |

### Infraestrutura

- VPS + Docker Compose
- PostgreSQL + Redis
- Cloudflare CDN
- GitHub Actions CI/CD

### Métricas de Sucesso

- 10 tenants ativos
- 100+ agendamentos reais processados
- NPS ≥ 60
- Zero downtime crítico

---

## 17.3 V1 — Lançamento Comercial (Mês 3–9)

### Objetivo: Monetizar e atingir 200 tenants.

### Funcionalidades

| Módulo | Entregas |
|--------|----------|
| **Pagamentos** | Gateway (Stripe/PagSeguro), PIX, sinal, webhook |
| **Planos** | Starter, Pro, Business (cobrança recorrente) |
| **CRM** | Ficha do cliente, histórico, preferências |
| **Personalização** | Domínio próprio, galeria de fotos, redes sociais, SEO |
| **Painel Admin** | Dashboard financeiro, relatórios básicos, exportação |
| **Site Público** | Página "Sobre", FAQ, depoimentos |
| **Auth** | Confirmação de e-mail, 2FA (opcional) |
| **Notificações** | E-mail, lembretes adicionais (1h antes) |
| **Super Admin** | Dashboard de plataforma, gestão de tenants e planos |

### Infraestrutura

- Kubernetes (managed) + Helm
- Managed PostgreSQL + Redis
- Prometheus + Grafana

### Métricas de Sucesso

- 200 tenants pagantes
- MRR ≥ R$ 18.000
- Churn ≤ 5%
- Uptime ≥ 99.9%

---

## 17.4 V2 — Expansão de Segmentos (Mês 9–18)

### Objetivo: Expandir para novos segmentos, atingir 1.000 tenants.

### Funcionalidades

| Módulo | Entregas |
|--------|----------|
| **Multi-segmento** | Templates por segmento (barbearia, salão, clínica, etc.) |
| **Relatórios** | Avançados (ocupação, retenção, ticket médio, origem) |
| **Promoções** | Cupons, descontos, campanhas segmentadas |
| **Fidelidade** | Programa de pontos, indicação |
| **Galeria** | Mídia avançada, fotos de resultados |
| **Agendamento** | Recorrente, múltiplos serviços, lista de espera |
| **Mobile** | PWA com notificações push |
| **Painel Admin** | Dashboard customizável, multi-idioma (pt-BR) |

### Infraestrutura

- Read replicas PostgreSQL
- Redis Cluster
- CDN multi-region (se necessário)

### Métricas de Sucesso

- 1.000 tenants pagantes
- MRR ≥ R$ 100.000
- 5+ segmentos suportados
- NPS ≥ 70

---

## 17.5 V3 — Plataforma (Mês 18–36)

### Objetivo: Virar plataforma, atingir 5.000 tenants.

### Funcionalidades

| Módulo | Entregas |
|--------|----------|
| **Multi-Unidade** | Redes e franquias, visão consolidada |
| **Marketplace** | API para desenvolvedores, apps de terceiros |
| **Public API** | REST API documentada, API keys, rate limits |
| **Integrações** | Google Calendar, Instagram, Facebook Ads |
| **Pagamentos** | Split de pagamento (comissão), múltiplos gateways |
| **Enterprise** | SSO, SLA, onboarding dedicado, CSS customizado |
| **Mobile** | App nativo (iOS + Android) |

### Infraestrutura

- AWS/GCP (Multi-AZ)
- Disaster Recovery cross-region
- ArgoCD (GitOps)

### Métricas de Sucesso

- 5.000 tenants pagantes
- MRR ≥ R$ 500.000
- 20+ apps no marketplace
- Expansão América Latina

---

## 17.6 V4 — Liderança de Mercado (Mês 36–60)

### Objetivo: Ser líder brasileiro, atingir 10.000+ tenants.

### Funcionalidades

| Módulo | Entregas |
|--------|----------|
| **AI/ML** | Previsão de demanda, precificação dinâmica, recomendação de serviços |
| **i18n** | Múltiplos idiomas (es, en), moedas, gateways locais |
| **Chatbot** | Atendimento automático via WhatsApp/chat |
| **BI** | Business Intelligence integrado |
| **White-label avançado** | Templates ilimitados, editor drag-and-drop |

### Métricas de Sucesso

- 10.000+ tenants pagantes
- MRR ≥ R$ 1.000.000
- Presente em 3+ países
- Valuation ≥ R$ 100M (IPO ou M&A)

---

## 17.7 Resumo por Versão

| | MVP | V1 | V2 | V3 | V4 |
|---|:---:|:--:|:--:|:--:|:--:|
| **Meses** | 0–3 | 3–9 | 9–18 | 18–36 | 36–60 |
| **Tenants** | 10 | 200 | 1.000 | 5.000 | 10.000+ |
| **MRR** | R$ 0 | R$ 18K | R$ 100K | R$ 500K | R$ 1M+ |
| **Módulos** | 4 | 6 | 9 | 12 | 14 |
| **Segmentos** | 1 (barbearia) | 3 | 5+ | Todos | Todos + intl |
| **Infra** | VPS | K8s | K8s + Replicas | Multi-AZ | Multi-Region |
| **Time** | 1 dev | 1 dev | 1-2 devs | 3-5 devs | 5+ devs |

---

> **Princípio:** Um roadmap não é uma promessa — é uma direção. As datas são estimativas e devem ser ajustadas conforme o feedback do mercado. O importante é que cada versão entregue valor real e incremental, nunca "big bang".
