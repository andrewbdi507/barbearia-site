# 🖥️ Painel Administrativo — Documentação

> **Versão:** 1.0.0 | **Data:** Julho 2026 | **Módulo:** `app.modules.admin` + `frontend/apps/admin`

---

## 1. Visão Geral

Painel administrativo completo inspirado em **Stripe Dashboard**, **Shopify Admin** e **Linear**. O cliente administra 100% do negócio sem desenvolvedor.

### 5 Diferenciais

| # | Diferencial | Descrição |
|---|-------------|-----------|
| **1** | **Dashboard Aggregator** | `GET /admin/dashboard` agrega KPIs de 6 módulos em 1 chamada |
| **2** | **Global Search ⌘K** | Busca unificada em clientes, serviços, profissionais. Atalho ⌘K |
| **3** | **Dynamic Config** | Alterações refletem instantaneamente. Zero deploy |
| **4** | **Breadcrumb + Command Palette** | Navegação contextual + atalhos de teclado |
| **5** | **Skeleton Loading + Empty States** | UX profissional em todos os estados |

---

## 2. Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                PAINEL ADMINISTRATIVO                     │
│                                                          │
│  Frontend (React + TS + Tailwind + shadcn/ui)           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Dashboard │ │  Agenda  │ │Clientes  │ │ Serviços │  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│       │            │            │            │          │
│       └────────────┼────────────┼────────────┘          │
│                    │            │                        │
│           ┌────────▼────────────▼────────┐              │
│           │        ADMIN API             │              │
│           │  GET /admin/dashboard        │              │
│           │  GET /admin/search?q=        │              │
│           │  GET /admin/quick-stats      │              │
│           └────────┬─────────────────────┘              │
│                    │                                     │
│      ┌─────────────┼─────────────┐                      │
│      │             │             │                      │
│  ┌───▼───┐  ┌──────▼──────┐ ┌───▼─────┐               │
│  │Booking│  │  Customer   │ │Payment  │  ← Módulos     │
│  │Module │  │  Module     │ │Module   │    existentes  │
│  └───────┘  └─────────────┘ └─────────┘               │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Como o Painel Conversa com os Módulos

O `AdminDashboard` API agrega dados de TODOS os módulos:

```python
# GET /api/v1/admin/dashboard
booking_repo = BookingRepository(session)
staff_repo = StaffRepository(session)
customer_repo = CustomerRepository(session)
review_repo = ReviewRepository(session)
payment_repo = PaymentRepository(session)
# → KPIs, timeline, staff_performance, week_revenue
```

Cada módulo mantém sua própria API (`/scheduling/bookings`, `/customers`, etc.). O Admin API apenas agrega e enriquece.

---

## 4. UX para Usuários Não-Técnicos

| Técnica | Descrição |
|---------|-----------|
| **Skeleton loading** | Placeholders animados enquanto carrega |
| **Empty states** | Mensagem amigável + call-to-action quando não há dados |
| **Feedback visual** | Cores de status (verde=confirmado, amarelo=em andamento) |
| **⌘K search** | Atalho universal. Digita nome do cliente e vai direto |
| **Breadcrumb** | Sempre sabe onde está. Navegação com 1 clique |
| **Dark mode** | Alternância com 1 clique. Respeita preferência do SO |
| **Mobile-first** | Sidebar colapsável. Cards responsivos (1→2→4 colunas) |

---

## 5. Escalabilidade

| Estratégia | Descrição |
|------------|-----------|
| **Paginação** | Todas as listagens com offset/limit |
| **Skeleton loading** | Renderização instantânea, dados chegam depois |
| **Code splitting** | React.lazy() por página. Só carrega o que precisa |
| **Cache TanStack Query** | Dados cacheados no frontend por 5 min |
| **Aggregated API** | 1 chamada = dashboard completo. Sem waterfall |
