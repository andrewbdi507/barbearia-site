# PLANO DE EVOLUÇÃO & ROADMAP — Barbershop SaaS

---

## VISÃO DE LONGO PRAZO

Transformar o Barbershop SaaS de uma plataforma de agendamento para um **Sistema Operacional completo para negócios baseados em horários** (barbearias, salões, clínicas, estúdios, consultórios).

```
2026 ──────────── 2027 ──────────── 2028 ──────────── 2029+
Plataforma       Expansão         Enterprise        Ecossistema
Agendamento      Multi-vertical   Global            Marketplace
```

---

## ROADMAP

### 🔴 v1.0.1 — HOTFIX (1 semana) — Build & Run

**Objetivo:** Sistema compila, roda e passa nos testes.

| Tarefa | Prioridade | Esforço |
|--------|:----------:|:-------:|
| Criar `app/presentation/api/app.py` (entry point) | 🔴 | 4h |
| Criar `app/infrastructure/database/session.py` | 🔴 | 2h |
| Adicionar `TokenExpiredError` em exceptions | 🔴 | 10min |
| Adicionar `jwt_algorithm` em SecuritySettings | 🔴 | 5min |
| Atualizar Dockerfile para `app.presentation.api.app:create_app` | 🔴 | 5min |
| Atualizar `pyproject.toml` packages para `["app"]` | 🔴 | 5min |
| Corrigir Alembic `env.py` para importar de `app.*` | 🔴 | 1h |
| Corrigir `tenant_service` em dependencies.py | 🔴 | 2h |
| Build & test: verificar todos os módulos carregam | 🔴 | 2h |
| Adicionar `__init__.py` ao módulo marketing | 🟢 | 1min |

---

### 🟡 v1.1 — GO LIVE (2-3 semanas) — Primeiros Clientes

**Objetivo:** Sistema funcional para os primeiros clientes pagantes.

| Feature | Esforço |
|---------|:-------:|
| Integrar MercadoPago SDK real (assinaturas + checkout) | 20h |
| Integrar Stripe SDK real | 20h |
| Implementar testes E2E reais (fluxo completo de negócio) | 30h |
| Conectar DashboardPage à API real (remover mocks) | 8h |
| Implementar AgendaPage funcional (calendário + bookings) | 16h |
| Implementar ClientsPage com dados reais | 8h |
| Implementar ServicesPage CRUD real | 8h |
| Implementar FinancialPage com dados reais | 8h |
| Rate limit Redis sliding window middleware | 8h |
| CSRF double-submit cookie pattern | 4h |
| Seed de planos iniciais (Starter, Pro, Premium, Enterprise) | 2h |
| Páginas de erro (404, 500) | 4h |
| Estados vazios em todas as listas | 4h |
| Toast feedback após ações (CRUD) | 4h |

---

### 🟢 v1.2 — ESTABILIZAÇÃO (1 mês) — Qualidade

**Objetivo:** Plataforma estável, performática e bem testada.

| Feature | Esforço |
|---------|:-------:|
| Materialized views para analytics KPIs | 16h |
| Redis cache para Customer 360° profile | 8h |
| Background job para processamento de imagens | 8h |
| Testes de carga (k6 — 4 cenários) | 16h |
| PgBouncer para connection pooling | 8h |
| CDN (Cloudflare) para uploads/imagens | 4h |
| Lazy loading de rotas no frontend | 4h |
| Otimização de fontes (self-host) | 2h |
| Acessibilidade (axe DevTools audit + correções) | 8h |
| Refatorar marketing para Pydantic models | 4h |

---

### 🔵 v1.3 — EXPANSÃO (2 meses) — Funcionalidades

**Objetivo:** Features que aumentam retenção e ticket médio.

| Feature | Esforço |
|---------|:-------:|
| Integrar WhatsApp Cloud API real (lembretes, confirmações) | 20h |
| Programa de fidelidade avançado (pontos, resgates) | 24h |
| Relatórios avançados (exportação PDF, agendamento de relatórios) | 24h |
| Integração Google Calendar (sync 2-way) | 16h |
| Check-in digital (QR Code) | 16h |
| Pesquisa de satisfação pós-atendimento (NPS) | 12h |
| Módulo de estoque/produtos (venda de produtos na barbearia) | 30h |
| App PWA para cliente final (instalar no celular) | 16h |

---

### 🟣 v2.0 — ENTERPRISE (3-4 meses) — Escala

**Objetivo:** Suporte a milhares de tenants com alta disponibilidade.

| Feature | Esforço |
|---------|:-------:|
| Migração para Kubernetes (EKS/GKE) | 40h |
| GitOps com ArgoCD | 16h |
| Multi-region (latência global) | 40h |
| Read replicas para analytics | 16h |
| Redis Cluster | 16h |
| Event sourcing com Kafka (eventos de negócio) | 40h |
| Service Mesh (Istio) para observabilidade avançada | 24h |
| Auto-scaling (HPA + KEDA) | 16h |
| Disaster recovery multi-region | 24h |

---

### 📱 v2.1 — MOBILE (3 meses) — App Nativo

| Feature | Esforço |
|---------|:-------:|
| App React Native para Admin (iOS + Android) | 120h |
| App React Native para Cliente Final (booking) | 80h |
| Push notifications nativas | 16h |
| Offline mode (agenda offline) | 40h |

---

### 🌍 v2.2 — INTERNACIONALIZAÇÃO (2 meses)

| Feature | Esforço |
|---------|:-------:|
| i18n (inglês, espanhol) — backend + frontend | 40h |
| Moedas múltiplas (USD, EUR, ARS) | 16h |
| Timezones por tenant | 8h |
| Gateways de pagamento regionais (MercadoPago LATAM, Stripe Global, Pix BR) | 24h |

---

### 🏪 v3.0 — MARKETPLACE (Longo Prazo)

| Feature | Descrição |
|---------|-----------|
| API Pública | REST API documentada para third-party developers |
| Marketplace de Plugins | Apps que estendem a plataforma (ex: integração com Instagram, CRM externo) |
| Temas comunitários | Marketplace de temas visuais white-label |
| Webhooks configuráveis | Clientes configuram webhooks para eventos de negócio |
| SDK JavaScript | Embed de booking em sites externos |

---

## CRONOGRAMA VISUAL

```
Mês 1     Mês 2     Mês 3     Mês 4-6     Mês 7-12    Ano 2+
─────────┬─────────┬─────────┬───────────┬───────────┬─────────
v1.0.1   v1.1      v1.2      v1.3        v2.0        v3.0
HOTFIX   GO LIVE   ESTABIL.  EXPANSÃO    ENTERPRISE  ECOSYSTEM
```

---

## MÉTRICAS DE SUCESSO

| Marco | Métrica | Alvo |
|-------|---------|:----:|
| **Go Live** | Primeiros 10 tenants pagantes | Mês 2 |
| **Product-Market Fit** | 50 tenants, < 5% churn mensal | Mês 4 |
| **Tração** | 200 tenants, NPS > 40 | Mês 8 |
| **Escala** | 1.000 tenants, 99.5% uptime | Ano 2 |
| **Enterprise** | 5.000+ tenants, multi-region | Ano 3 |

---

## RISCOS DO ROADMAP

| Risco | Mitigação |
|-------|-----------|
| SDKs de pagamento complexos (certificação, compliance) | Começar com Stripe (mais simples). Adicionar MercadoPago depois. |
| Frontend demandar mais tempo que o estimado | Priorizar páginas core (Agenda, Clientes, Serviços). Deixar analytics para v1.2. |
| Custo de infra subir com escala | Cloudflare free tier + VPS até 500 tenants. Migrar para cloud gerenciada apenas quando necessário. |
| Concorrência copiar features | Velocidade de execução é a vantagem. Focar em NPS e retenção. |
