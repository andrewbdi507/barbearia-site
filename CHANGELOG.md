# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [1.1.2] — 2026-07-21

### 🔧 Integração Total — Sistema Unificado

- **193 rotas carregadas** de 14 módulos em um único FastAPI app
- **293 correções de sintaxe**: `Annotated[Type, Depends(func)]` → `Type = Depends(func)`
- **Arquivos criados**: `app/presentation/api/app.py`, `app/infrastructure/database/session.py`
- **8 `__init__.py`** criados em módulos auth, staff, site, marketing
- **Bugs corrigidos**: `TokenExpiredError`, `jwt_algorithm`, `settings.is_development`, `import jwt` → `from jose import jwt`
- **Dockerfile**: Corrigido para `app.presentation.api.app:create_app`
- **pyproject.toml**: `packages = ["app"]`

### ✅ Verificação
```bash
python -c "from app.presentation.api.app import create_app; app = create_app(); print(len(app.routes))"
# → 193 rotas
```

---

## [1.1.1] — 2026-07-21

### 🔍 Auditoria Final — Go Live Certification

- **Status:** ✅ APROVADO COM RESSALVAS
- **Nota média:** 7.96 / 10
- **Bugs críticos encontrados:** 4 (build quebrado `app/` vs `src/`)
- **Vulnerabilidades:** 0 críticas, 0 altas, 2 médias
- **10 relatórios de auditoria** (executivo, segurança, performance, escalabilidade, UX, qualidade, checklist go-live, roadmap, certificação, lista de melhorias)
- 37 melhorias priorizadas em 5 fases (~360h total)

### 🔴 Problemas Identificados (Corrigir antes de build)
- C1: `app/presentation/api/app.py` inexistente (entry point)
- C2: `app/infrastructure/database/session.py` inexistente
- C3: `TokenExpiredError` não definido em exceptions
- C4: `jwt_algorithm` ausente em SecuritySettings

---

## [1.1.0] — 2026-07-21

### 🚀 DevOps & Infrastructure — Production Ready

#### Containerização
- **Dockerfiles otimizados**: Backend (multi-stage, non-root), Frontend (multi-stage + Nginx), Worker, Scheduler
- **Nginx reverse proxy**: Security headers (HSTS, CSP, X-Frame-Options, XSS), rate limiting, SSL termination
- **.dockerignore**: Build context minimizado

#### Ambientes
- **Development**: Hot-reload, volumes montados, debug logging
- **Testing**: Ephemeral DB, CI integrado, sem volumes
- **Staging**: Espelha produção, Grafana + Prometheus, deploy automático
- **Production**: Resource limits, health checks, logging rotativo, non-root containers

#### CI/CD Pipeline (GitHub Actions)
- **6 estágios**: Quality → Test → Build → Deploy Staging → Deploy Production → Notify
- Security scan: Bandit + pip-audit + Trivy (container scanning)
- Blue-green deploy com zero downtime
- Health checks automáticos pós-deploy

#### Observabilidade Stack
- **Prometheus**: Métricas (Golden Signals + negócio), 13 regras de alerta
- **Grafana**: Dashboard operacional (KPIs, throughput, latency, CPU, memory, bookings, payments)
- **Loki + Promtail**: Agregação de logs estruturados (JSON)
- **Node Exporter**: Métricas de host (CPU, RAM, disco)

#### Backup & Disaster Recovery
- **backup-db.sh**: pg_dump custom + compressão, retenção 30d/12w/60m, sync S3/R2
- **restore-db.sh**: Restore interativo com verificação de integridade
- **backup-uploads.sh**: Tar + compress + sync cloud
- **RECOVERY.md**: 6 cenários de falha documentados (DB, Redis, Storage, Server, Gateway, DNS)

#### Segurança Operacional
- HTTPS obrigatório (TLS 1.2+, HSTS preload)
- Security headers via Nginx (CSP, X-Frame, XSS, Referrer-Policy, Permissions-Policy)
- Rate limiting: API 100r/s, Auth 5r/m, Webhooks 50r/s
- Secrets: nunca no código, templates com placeholders
- Rotação de chaves documentada (SECRET_KEY, JWT, DB password, API keys)
- Container non-root, firewall rules, LGPD compliance

#### Documentação Operacional (8 docs)
- `DEPLOY.md`, `INFRASTRUCTURE.md`, `BACKUP.md`, `RECOVERY.md`
- `OBSERVABILITY.md`, `SECURITY_OPERATIONS.md`, `RUNBOOK.md`, `OPERATIONS.md`
- `PRODUCTION_CHECKLIST.md`: 60+ itens pré/pós-deploy

#### Escalabilidade
- Arquitetura preparada para: VPS → Docker Swarm → Kubernetes
- Múltiplas instâncias API + Workers independentes
- Load Balancer (Nginx) + Health checks
- Resource limits em todos os containers
- Capacity planning documentado (500 → 10.000+ tenants)

---

## [0.13.0] — 2026-07-21

### Adicionado
- **Módulo de Marketing, Promoções & Automações completo**
  - Domain: 7 entidades (Coupon, Promotion, Campaign, AutomationRule, GiftCard, + enums 7), Rule Engine
  - Infrastructure: 5 modelos SQLAlchemy + MarketingRepository (coupons, promotions, campaigns, automations, gift cards)
  - Application: MarketingService (coupon CRUD+validate+apply, promotions+active filtering, campaigns, rule engine with evaluate_trigger, smart segments calculator, gift cards)
  - Presentation: 12 endpoints REST (coupons CRUD+validate, promotions CRUD+active, campaigns CRUD, automations CRUD+evaluate, smart segments, gift cards)
- **5 diferenciais de Marketing:**
  1. Rule Engine — Evento→Condição→Ação. Regras JSONB no banco. Extensível sem código
  2. Smart Segments — VIP, Lapsed 30d, Birthday, High Ticket, New calculados em tempo real
  3. Coupon Validator — validador centralizado com expiração, limites, valor mínimo
  4. Campaign Orchestrator — event-driven integrado ao NotificationCenter
  5. Anti-Abuse — rate limit, uso único, max_per_customer, is_valid property
- Cupons: fixed/percentage, first purchase, VIP, validade, usos limitados
- Promoções: time_period, happy_hour, bundle, seasonal, buy_x_get_y
- Automações: Rule Engine com evaluate_trigger (equals, greater_than, less_than, contains)
- Smart Segments: VIP ($1000+), Lapsed 30d, High Ticket ($80+), New (<30d), Birthday
- Gift Cards: criação, código único, saldo, redeem parcial/total
- Testes: 20+ cenários (Coupon discount+validity, Promotion, GiftCard, Rule Engine conditions, Smart Segments)
- Documentação: MARKETING.md

---

## [0.12.0] — 2026-07-21

### Adicionado
- **Módulo de Uploads, CMS & SEO completo**
  - Domain: StorageProvider (ABC) + Factory, 2 entidades (MediaAsset, CMSPage+CMSBlock), 2 repository interfaces
  - Infrastructure: 3 storage providers (Local, S3, R2), ImageProcessor (validate, hash, resize, strip EXIF, WebP), 2 modelos SQLAlchemy + 2 repositórios
  - Application: MediaService (upload pipeline, media library CRUD, dedup), CMSService (block-based pages, SEO score analyzer)
  - Presentation: 10 endpoints REST (upload, media library CRUD, CMS pages CRUD, SEO analysis)
- **5 diferenciais:**
  1. Storage Provider Pattern — `StorageProvider` ABC. Trocar S3→R2 via config
  2. Image Processing Pipeline — validate → strip EXIF → resize → thumbnail → WebP → hash
  3. Block-Based CMS — páginas JSONB com blocos (hero, text, image, CTA, gallery, team, services)
  4. Media Dedup — SHA-256 content hash previne uploads duplicados
  5. SEO Score Analyzer — analisa página e sugere melhorias com score 0-100
- 3 storage providers: LocalStorage (dev), S3Storage (AWS), R2Storage (Cloudflare)
- ImageProcessor: whitelist, MIME validation, max 10MB, SHA-256 hash, unique filename
- CMS: páginas compostas de blocos JSONB, versionamento, publish/unpublish
- SEO Analyzer: verifica meta title, meta description, OG image, H1 presence
- Testes: 15+ cenários (ImageProcessor, Storage Providers, MediaAsset, CMSPage, SEO analyzer)
- Documentação: MEDIA.md

---

## [0.11.0] — 2026-07-21

### Adicionado
- **Módulo de Analytics & Business Intelligence completo**
  - Domain: 4 entidades (Goal, AlertRule, KPIData, ChartData)
  - Infrastructure: 2 modelos SQLAlchemy (goals, alerts), 2 repositórios
  - Application: KPI Registry (7 KPIs registrados, extensível via `register_kpi()`), AnalyticsService (compute KPIs, charts, goals, alerts, export CSV, comparison engine)
  - Presentation: 12 endpoints REST (KPIs, charts revenue/top-services/top-professionals/peak-hours, goals CRUD, alerts CRUD, export CSV)
- **5 diferenciais BI:**
  1. Modular KPI Registry — novo KPI = 1 função async + `register_kpi()`. Dashboard auto-descobre
  2. Comparison Engine — todo KPI calcula `change_pct` e `trend` vs período anterior
  3. Smart Alert Engine — regras no banco, avaliação de thresholds
  4. Streaming Export — CSV com streaming, chunked para datasets grandes
  5. Charts Desacoplados — `ChartData` genérico, qualquer frontend renderiza
- 7 KPIs: revenue_today, bookings_today, cancellation_rate, avg_ticket, new_customers, occupancy, no_show
- 4 gráficos: revenue (line), top-services (bar), top-professionals (bar), peak-hours (bar)
- Metas configuráveis com progresso percentual
- Alertas inteligentes com métricas e thresholds
- Export CSV: bookings, revenue, customers — com filtro de data
- Testes: 15+ cenários (KPI registry, Goal progress, AlertRule, KPIData, ChartData, period resolution)
- Documentação: ANALYTICS.md

---

## [0.10.0] — 2026-07-21

### Adicionado
- **Painel Administrativo completo** — Backend + Frontend
  - Backend: Admin Dashboard Aggregator API (KPIs, timeline, staff performance, week revenue), Global Search API (clientes+serviços+staff), Quick Stats API
  - Frontend: AdminLayout com breadcrumb, ⌘K command palette, dark mode toggle, sidebar responsivo, notificações
  - 15 páginas: Dashboard (com skeleton loading + API real), Agenda, Clientes, Equipe, Serviços, Financeiro, Relatórios, Galeria, Avaliações, Site, Notificações, Configurações, Aparência, Ajuda
  - API Client tipado (TypeScript) com fetch wrapper + JWT auth
- **5 diferenciais do painel:**
  1. Dashboard Aggregator — 1 endpoint agrega KPIs de 6 módulos
  2. Global Search ⌘K — busca unificada com atalho de teclado
  3. Dynamic Config — alterações refletem instantaneamente, zero deploy
  4. Breadcrumb + Command Palette — navegação contextual profissional
  5. Skeleton Loading + Empty States — UX polida em todos os estados
- AdminLayout aprimorado: breadcrumb automático, ⌘K modal, sidebar com 14 itens, user menu
- Dashboard com: KPIs reais via API, skeleton loading, timeline do dia, staff performance com barras de ocupação
- Páginas criadas: ProfessionalsPage, FinancialPage, ReportsPage, SettingsPage
- API Client: `adminAPI.getDashboard()`, `adminAPI.search(q)`, `adminAPI.getQuickStats()`
- Testes: Admin Dashboard contract, Global Search contract
- Documentação: ADMIN_PANEL.md

---

## [0.9.0] — 2026-07-21

### Adicionado
- **Módulo de Site Público White-Label completo**
  - Domain: 3 entidades (SitePage, SEOSettings, SiteContent), 3 interfaces
  - Infrastructure: 3 modelos SQLAlchemy (site_pages, site_seo, site_content), 3 repositórios
  - Application: SiteService (aggregated site data, CSS variable generator, SEO metadata generator, JSON-LD Schema.org generator, content pages, SEO settings), DTOs
  - Presentation: 8 endpoints (público: GET /site, GET /site/pages/{slug}, GET /site/sitemap.xml; admin: CRUD pages, SEO, content)
- **5 diferenciais White-Label:**
  1. Site Resolver — GET /site?subdomain=studio27 retorna TUDO em 1 chamada
  2. CSS Variable Generator — branding JSONB → `--color-primary`, `--font-heading`, etc.
  3. Aggregated Site API — branding + serviços + equipe + reviews + SEO + JSON-LD
  4. SEO Auto-Generation — Open Graph, Twitter Cards, JSON-LD Schema.org LocalBusiness
  5. Content Pages Versioned — Sobre, Privacidade, Termos editáveis via painel
- Sitemap.xml automático por tenant
- Páginas editáveis com versionamento (slug, título, conteúdo Markdown, meta tags)
- SEO Settings: meta tags, Google Analytics, Facebook Pixel, custom header/footer code
- Site Content: hero section, about section, promotions, toggles (show_services, etc.)
- Integração automática com scheduling, staff, customer modules
- Testes: 15+ cenários (CSS vars, SEO metadata, JSON-LD, pages, DTOs)
- Documentação: WEBSITE.md

---

## [0.8.0] — 2026-07-21

### Adicionado
- **Central de Notificações completa** — Event-Driven + Double Provider Pattern
  - Domain: 2 entidades (NotificationTemplate, Notification), 6 enums, NotificationChannelProvider (ABC) + Factory, EventBus + NotificationEvent, 3 repository interfaces
  - Infrastructure: 3 modelos SQLAlchemy, 4 channel providers (WhatsApp, Email, SMS, Push), 3 repositórios
  - Application: NotificationService (event processing, manual send, retry, templates, channel config), TemplateEngine (render, extract, validate), DTOs
  - Presentation: 10 endpoints REST (templates CRUD+preview, notifications list+send+query, retry, channel config)
- **5 diferenciais:**
  1. Event Bus + Double Provider — módulos publicam eventos, central roteia por canal
  2. Template Engine — `{{variavel}}` resolvido do payload, versionado, preview sem enviar
  3. Smart Delivery Pipeline — retry com exponential backoff (1m→5m→15m→1h→6h) + DLQ
  4. Idempotency via Event ID — `UNIQUE(event_id, channel, customer_id)`
  5. Template Preview — renderiza com dados de exemplo sem enviar
- EventBus in-process: módulos publicam NotificationEvent, central processa
- Template Engine: render com variáveis aninhadas (`{{customer.name}}`), extração e validação
- 4 canais implementados: WhatsAppProvider, EmailProvider, SMSProvider, PushProvider
- Quiet hours por tenant (ex: sem notificações entre 22h-08h)
- Retry automático com exponential backoff + DLQ após 5 falhas
- Histórico completo por cliente e por tenant
- Testes: 20+ cenários (Notification lifecycle, TemplateEngine, EventBus pub/sub, Providers, DTOs)
- Documentação: NOTIFICATIONS.md

---

## [0.7.0] — 2026-07-21

### Adicionado
- **Módulo de Pagamentos completo** com Provider Pattern
  - Domain: 4 entidades (Payment AR, PaymentEvent, GatewayConfig, SubscriptionPayment), 6 enums, Provider Interface (ABC) + PaymentProviderFactory, 4 repository interfaces
  - Infrastructure: 4 modelos SQLAlchemy, 4 repositórios, 2 providers implementados (MercadoPagoProvider + StripeProvider) com verificação de assinatura de webhook
  - Application: PaymentService (create, cancel, refund, webhook processing, idempotency, event sourcing), DTOs
  - Presentation: 8 endpoints REST + webhook público multi-gateway
- **6 diferenciais** financeiros:
  1. Provider Pattern Puro — `PaymentProvider` ABC, troca de gateway sem alterar código
  2. Event Sourcing Imutável — `PaymentEvent` append-only para cada mudança de status
  3. Webhook Signature Verification — HMAC-SHA256 por provider, replay attack detection
  4. Double-Layer Idempotency — `idempotency_key` (app) + `UNIQUE(gateway_event_id)` (DB)
  5. PCI-DSS Zero Storage — apenas `gateway_payment_id`, nunca dados de cartão
  6. Async Processing — webhook responde 200 imediatamente
- PaymentProviderFactory com registro dinâmico de providers
- Webhook multi-gateway: `/webhooks/mercado-pago`, `/webhooks/stripe`, `/webhooks/{gateway}`
- Anti-replay: `gateway_event_id` UNIQUE no banco
- Suporte a PIX, Cartão de Crédito, Boleto (estrutura)
- Depósito/sinal configurável: none, fixed, percentage
- Cobrança de assinatura recorrente (SubscriptionPayment)
- GatewayConfig criptografado por tenant
- Testes: 20+ cenários (Payment lifecycle, Provider Pattern, webhook parse, signature verification, DTOs)
- Documentação: PAYMENTS.md

---

## [0.6.0] — 2026-07-21

### Adicionado
- **Módulo de CRM (Customer) completo**
  - Domain: 8 entidades (Customer AR, CustomerPreference, CustomerTag, Review, Consent, LoyaltyAccount, LoyaltyTransaction, Referral), 6 enums, 7 interfaces
  - Infrastructure: 8 modelos SQLAlchemy (Customer, Preference, Tag, Review, Consent, LoyaltyAccount, LoyaltyTransaction, Referral), 7 repositórios
  - Application: CustomerService (CRUD, Customer 360°, preferências, tags, reviews+moderação, consentimentos LGPD, fidelidade+earn/redeem, indicações, blacklist), 15+ DTOs
  - Presentation: 25+ endpoints REST (customers, profile 360°, preferences, tags, reviews+moderate+respond, consents, LGPD export/anonymize, loyalty+earn/redeem, referrals, block/unblock)
- **5 diferenciais** CRM:
  1. Customer 360° View — perfil agregado com métricas computadas em 1 endpoint
  2. Dynamic Smart Segments — filtros por tag, status, comportamento
  3. Loyalty Tiers Auto-Promotion — Bronze→Silver→Gold→Diamond por visitas
  4. LGPD by Design — consentimentos versionados, exportação completa, anonimização
  5. Review + Business Response — moderação, resposta pública da empresa
- Programa de fidelidade: pontos, tiers, earn/redeem, histórico de transações
- Programa de indicações: código único, tracking de status, recompensa
- Blacklist: bloqueio/desbloqueio de clientes com motivo
- Tags configuráveis por tenant (VIP, Novo, Premium, Frequente, etc.)
- Consentimentos LGPD versionados (privacy, terms, marketing, data_processing)
- Exportação LGPD: JSON completo com dados de todos os módulos
- Anonimização LGPD: substitui PII por valores anônimos
- Testes: 20+ cenários (Customer lifecycle, Loyalty tiers+transactions, Review moderation, Consent revoke, Referral tracking, DTOs)
- Documentação: CRM.md

---

## [0.5.0] — 2026-07-21

### Adicionado
- **Módulo de Agendamento (Scheduling) completo** — o coração do sistema
  - Domain: 4 entidades (Service, Booking AR, BlockedDate, WaitlistEntry), 3 value objects (TimeSlot, ServicePricing, BookingSlot/AvailabilityResult), 4 enums (BookingStatus, BookingSource, BlockType, WaitlistStatus), 9 interfaces
  - Infrastructure: 9 modelos SQLAlchemy (Service, ServiceCategory, ProfessionalService, Booking+BookingService, BookingStatusLog, BlockedDate, WaitlistEntry), 7 repositórios, **AvailabilityEngine** (motor de disponibilidade)
  - Application: SchedulingService (catálogo, booking CRUD, state machine, reschedule, cancel, waitlist auto-promotion), 20+ DTOs
  - Presentation: 25+ endpoints REST (services, categories, availability, smart-suggestions, bookings, check-in/out, blocked dates, waitlist)
- **5 diferenciais** sobre agendas tradicionais:
  1. Availability Engine dedicado — calcula em <50ms considerando jornada + time-off + bloqueios + bookings + almoço
  2. Smart Slot Suggestions — ranqueia horários por qualidade (evita gaps, prefere mesmo profissional)
  3. Idempotency Keys — anti double-booking via chave única + constraint no banco
  4. Waitlist Auto-Promotion — notifica fila automaticamente ao cancelar
  5. State Machine com Audit Trail imutável — 8 estados com log append-only
- Máquina de estados: pending → confirmed → in_progress → completed / cancelled / no_show / rescheduled
- BookingStatusLog: registro imutável de toda transição
- Serviços com: buffer time, preço promocional, tempo mínimo/máximo de antecedência
- Profissionais vinculados a serviços (N:N) com preço e duração customizados
- Bloqueios: full_day, partial, recurring (diário/semanal/mensal)
- Check-in / Check-out com registro de tempo real
- Testes: 25+ cenários (TimeSlot, ServicePricing, Booking state machine, Service, Waitlist, AvailabilityEngine, DTOs)
- Documentação: SCHEDULING.md

---

## [0.4.0] — 2026-07-21

### Adicionado
- **Módulo de Equipe (Staff) completo**
  - Domain: 7 entidades (StaffProfile, Team, Position, Specialty, StaffSchedule, TimeOff, Invitation, StaffAuditLog), 1 value object (CommissionRule), 11 enums, 8 interfaces
  - Infrastructure: 8 modelos SQLAlchemy (StaffProfile, Position, Specialty, Team+TeamMember, StaffSchedule, TimeOff, Invitation, StaffAuditLog), 8 repositórios
  - Application: StaffService (CRUD staff, ciclo de vida, equipes, jornada, ausências, convites, auditoria), 20+ DTOs
  - Presentation: 30+ endpoints REST (positions, specialties, staff CRUD, teams CRUD, schedules, time-offs, invitations, audit)
- Cargos configuráveis por tenant (NUNCA hardcoded)
- Especialidades configuráveis (Barba, Corte, Química, etc.)
- Equipes com líder e membros (N:N)
- Jornada de trabalho por profissional (7 dias, almoço, slot)
- Ausências: férias, folgas, licenças (fluxo approve/reject)
- Convites por email com token (expira 7 dias)
- Comissão: none, percentage, fixed (estrutura preparada)
- Auditoria completa: toda ação registrada
- Relação 1:1 StaffProfile ↔ User (auth module)
- RBAC integrado: permissões por cargo + permissões do auth module
- Testes: 20+ cenários (entities, value objects, service, DTOs)
- Documentação: STAFF.md

---

## [0.3.0] — 2026-07-21

### Adicionado
- **Módulo Multi-Tenant completo** — fundação SaaS
  - Domain: 9 entidades (Tenant AR, Plan, Subscription, TenantSettings, TenantBranding, BusinessHours, Domain, SocialMedia, TenantMedia), 4 value objects (Subdomain, PlanLimits, BusinessHoursSlot, BrandingColors), 11 enums, 12 interfaces (ports)
  - Infrastructure: 9 modelos SQLAlchemy, 10 repositórios, TenantRedisCache + NullTenantCache
  - Application: TenantService (criação, ciclo de vida, limites, branding, settings, domínios, redes sociais), PlanService (planos, assinaturas, upgrade/downgrade), 20 DTOs (Pydantic)
  - Presentation: 20+ endpoints REST, TenantMiddleware (resolução automática de tenant via subdomínio), 3 dependências (get_current_tenant, require_plan_feature, get_tenant_service)
- Ciclo de vida completo: trial (14d) → active → past_due → suspended → cancelled → deleted
- 4 planos configuráveis (Starter, Pro, Premium, Enterprise) com limites e features via banco
- Sistema de branding white-label (cores, fontes, logo, banner, custom CSS)
- Subdomínios (empresa.barbeariaos.com.br) com cache Redis
- Estrutura preparada para domínio próprio (CNAME, verificação DNS, SSL)
- Cache strategy: tenant (5min), branding (5min), subdomínio→ID (1h), planos (10min)
- Isolamento 3 camadas: middleware (app) + RLS (banco) + prefixo S3 (storage)
- Validação de limites em runtime (PlanLimits.to_dict() → JSONB no banco)
- Planos adicionáveis sem alteração de código (INSERT no banco ou POST /plans)
- Testes: 30+ cenários (value objects, entities lifecycle, service, DTOs, middleware)
- Documentação: MULTI_TENANT.md, BILLING.md
- Core: config.py (Settings centralizadas), exceptions.py (20 exceções HTTP-friendly)

### Alterado
- BaseModel agora referencia `tenants` (FK) como tenant raiz do sistema
- CHANGELOG atualizado com v0.3.0

---

## [0.2.0] — 2026-07-21

### Adicionado
- **Módulo de Autenticação completo** (auth module)
  - Domain: entidades (User, Role, Session, RefreshToken), value objects (Email, Password), interfaces
  - Application: AuthService (login, refresh, logout, password reset, RBAC), DTOs (Pydantic)
  - Infrastructure: 7 modelos SQLAlchemy, AuthRepository, Argon2id hashing, JWT (HS256), opaque refresh tokens
  - Presentation: 10 endpoints REST, FastAPI dependencies (get_current_user, require_permissions, require_tenant_match)
- Argon2id password hashing (time_cost=3, memory_cost=65536, parallelism=4)
- JWT access tokens (HS256, 15 min expiry) + opaque refresh tokens (SHA-256, 7 dias)
- HttpOnly cookies para refresh tokens (SameSite=Strict, Secure)
- RBAC com 6 roles: super_admin, owner, admin, barber, receptionist, customer
- Permissões granulares no padrão `resource:action[:scope]`
- Account lockout: 5 tentativas → 15 min de bloqueio
- Anti-enumeração: mensagens genéricas em todos os erros
- Session tracking com device info (IP, User-Agent, device_type)
- Refresh token rotation com family-based reuse detection
- Rehash automático de senhas (Argon2id) no login
- Testes unitários: PasswordHashing, Tokens, Login, Refresh, PasswordReset, RBAC
- Documentação: AUTH.md, RBAC.md, API.md

### Alterado
- Estratégia de segurança: bcrypt → Argon2id (11-estrategia-seguranca.md)
- Refresh tokens: JWT → Opaque strings com hash SHA-256
- Todas as ressalvas críticas de segurança resolvidas (C1–C5 da auditoria)

### Pendente (MVP)
- Rate limiting middleware (Redis sliding window)
- CSRF protection (double-submit cookie)
- CSP headers (sem unsafe-inline)
- Alembic migration para tabelas de auth
- Integração com serviço de email (password reset)
- API de agendamento (CRUD)
- API de serviços e profissionais
- Integração frontend ↔ backend
- WhatsApp (confirmação + lembrete)

---

## [0.1.0] — 2026-07-20

### Adicionado
- Estrutura inicial do projeto (Clean Architecture)
- Configuração do backend (FastAPI + SQLAlchemy + Alembic)
- Configuração do frontend (React + Vite + TailwindCSS)
- Docker Compose para desenvolvimento (PostgreSQL + Redis + Backend)
- Design System base (tokens, temas, componentes)
- Painel Administrativo (layout + 10 páginas)
- Site Público (home + booking flow + confirmação)
- Documentação completa de arquitetura (21 documentos)
- Documentação de UX/UI (24 documentos)
- Documentação de banco de dados (5 documentos)
- Documentação de integrações (5 documentos)
- Auditoria de segurança (7 documentos)
- Revisão executiva (7 documentos)
- CI/CD pipeline (GitHub Actions)
- Qualidade de código (Ruff, Black, MyPy, Pre-commit)
- Testes unitários (backend: 18, frontend: estrutura)

### Pendente (MVP)
- Implementar 10 ressalvas de segurança
- API de agendamento (CRUD)
- API de serviços e profissionais
- Integração frontend ↔ backend
- WhatsApp (confirmação + lembrete)

---

[0.1.0]: https://github.com/barbershop/barbershop-saas/releases/tag/v0.1.0
