# LISTA PRIORIZADA DE MELHORIAS — Barbershop SaaS

**Ordenado por:** Impacto × Urgência / Esforço

---

## 🔴 BLOQUEANTES (Antes de qualquer deploy)

| # | Melhoria | Esforço | Impacto |
|---|----------|:------:|:-------:|
| 1 | Criar `app/presentation/api/app.py` (entry point) | 4h | 🔴 Sistema inicia |
| 2 | Criar `app/infrastructure/database/session.py` | 2h | 🔴 DB funciona |
| 3 | Adicionar `TokenExpiredError` em `app/core/exceptions.py` | 10min | 🔴 Auth funciona |
| 4 | Adicionar `jwt_algorithm` em `SecuritySettings` | 5min | 🔴 JWT funciona |
| 5 | Atualizar Dockerfile (referência `app.*` não `src.*`) | 5min | 🔴 Build funciona |
| 6 | Atualizar `pyproject.toml` packages para `["app"]` | 5min | 🔴 Build funciona |
| 7 | Corrigir Alembic `env.py` para `app.*` | 1h | 🔴 Migrations |

**Total Bloqueantes:** ~8 horas

---

## 🟠 PRÉ-GO LIVE (Antes de clientes pagantes)

| # | Melhoria | Esforço | Impacto |
|---|----------|:------:|:-------:|
| 8 | Integrar Stripe SDK real | 20h | 🟠 Pagamentos |
| 9 | Integrar MercadoPago SDK real | 20h | 🟠 Pagamentos BR |
| 10 | Corrigir `tenant_service` global (None → instância) | 2h | 🟠 Multi-tenant |
| 11 | Seed de planos (Starter, Pro, Premium, Enterprise) | 2h | 🟠 Onboarding |
| 12 | Conectar DashboardPage à API real | 8h | 🟠 Admin funcional |
| 13 | Conectar AgendaPage à API real | 16h | 🟠 Core funcional |
| 14 | Rate limit Redis sliding window | 8h | 🟠 Segurança |
| 15 | CSRF double-submit cookie | 4h | 🟠 Segurança |

**Total Pré-Go Live:** ~80 horas (2 semanas)

---

## 🟡 PÓS-GO LIVE (Primeiras 4 semanas)

| # | Melhoria | Esforço | Impacto |
|---|----------|:------:|:-------:|
| 16 | Implementar testes E2E reais | 30h | 🟡 Qualidade |
| 17 | Conectar ClientsPage, ServicesPage, FinancialPage | 24h | 🟡 Admin |
| 18 | Toast feedback (sucesso/erro após ações) | 4h | 🟡 UX |
| 19 | Estados vazios (EmptyState) em listas | 4h | 🟡 UX |
| 20 | Páginas 404/500 personalizadas | 4h | 🟡 UX |
| 21 | `boto3` nas dependências (S3 real) | 5min | 🟡 Storage |
| 22 | `__init__.py` no módulo marketing | 1min | 🟡 Consistência |

**Total Pós-Go Live:** ~66 horas (2-3 semanas)

---

## 🟢 ESTABILIZAÇÃO (v1.2)

| # | Melhoria | Esforço | Impacto |
|---|----------|:------:|:-------:|
| 23 | Materialized views analytics | 16h | 🟢 Performance |
| 24 | Redis cache Customer 360° profile | 8h | 🟢 Performance |
| 25 | Background job image processing | 8h | 🟢 Performance |
| 26 | Testes de carga (k6) | 16h | 🟢 Confiabilidade |
| 27 | PgBouncer connection pooling | 8h | 🟢 Escala |
| 28 | Lazy loading rotas frontend | 4h | 🟢 Performance |
| 29 | Acessibilidade (axe audit + fixes) | 8h | 🟢 Inclusão |
| 30 | Refatorar marketing → Pydantic models | 4h | 🟢 Consistência |

**Total Estabilização:** ~72 horas (2-3 semanas)

---

## 🔵 EXPANSÃO (v1.3+)

| # | Melhoria | Esforço |
|---|----------|:------:|
| 31 | WhatsApp Cloud API real | 20h |
| 32 | Programa de fidelidade avançado | 24h |
| 33 | Integração Google Calendar sync | 16h |
| 34 | Check-in digital (QR Code) | 16h |
| 35 | Pesquisa NPS pós-atendimento | 12h |
| 36 | Módulo de estoque/produtos | 30h |
| 37 | PWA para cliente final | 16h |

---

## 📊 DISTRIBUIÇÃO POR FASES

```
Fase           Horas    Itens   Dependências
────────────   ─────    ─────   ────────────
BLOQUEANTES     8h       7      Nenhuma
PRÉ-GO LIVE    80h       8      Bloqueantes
PÓS-GO LIVE    66h       7      Pré-Go Live
ESTABILIZAÇÃO  72h       8      Pós-Go Live
EXPANSÃO      134h       7      Estabilização
────────────   ─────    ─────
TOTAL         360h      37
```

**Tempo total estimado para todas as melhorias:** ~360 horas (9 semanas, 1 desenvolvedor full-time)
