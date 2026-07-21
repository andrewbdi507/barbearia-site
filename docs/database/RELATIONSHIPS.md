# 03 — Relationships (Relacionamentos)

> Mapa completo de relacionamentos, cardinalidades e dependências entre todas as 47 entidades.

---

## 1. Diagrama de Relacionamentos (Visão Consolidada)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        PLATFORM CONTEXT                                   │
│                                                                           │
│  Plan (1) ──────── (N) Subscription (N) ──────── (1) Tenant              │
│                                                       │                   │
│  PlatformUser (independente — super admin)            │                   │
│  FeatureFlag (independente)                           │                   │
└───────────────────────────────────────────────────────┼───────────────────┘
                                                        │
        ┌───────────────────────────────────────────────┤
        │                                               │
        ▼                                               ▼
┌──────────────────────┐                    ┌──────────────────────┐
│    TENANT CONTEXT    │                    │    AUTH CONTEXT       │
│                      │                    │                       │
│  TenantSettings(1:1) │                    │  Role (N) ←── (N)    │
│  TenantBranding(1:1) │                    │    ↑         UserRole │
│  BusinessHours(1:N)  │                    │    │           ↓      │
│  Domain(1:N)         │                    │    └─── (N) User      │
│  SocialMedia(1:N)    │                    │         │             │
│  Media(1:N)          │                    │         ├── Session   │
│  SEOSettings(1:1)    │                    │         ├── RefreshT. │
│  GatewayConfig(1:N)  │                    │         ├── PwdReset  │
└──────────────────────┘                    │         │             │
                                            └─────────┼─────────────┘
                                                      │
        ┌─────────────────────────────────────────────┤
        │                                             │
        ▼                                             ▼
┌──────────────────────┐                  ┌──────────────────────┐
│ SCHEDULING CONTEXT   │                  │  CUSTOMER CONTEXT    │
│                      │                  │                       │
│  ServiceCategory     │                  │  Customer             │
│       │              │                  │    ├── Preference(1:1)│
│       ▼              │                  │    ├── Loyalty(1:1)   │
│  Service ←─(N:N)─→ Professional         │    ├── LoyaltyTxn     │
│       │       (N:N via ProfessionalServ)│    ├── Referral       │
│       │              │                  │    ├── Review         │
│       │              │                  │    └── Consent        │
│       ▼              ▼                  │                       │
│  ┌─────────────────────────┐            │                       │
│  │       BOOKING (AR)      │            │                       │
│  │                         │            │                       │
│  │  ┌── BookingService     │            │                       │
│  │  ├── BookingStatusLog   │            │                       │
│  │  ├── Payment (1:1)      │            │                       │
│  │  └── Review (1:1)       │            │                       │
│  └─────────────────────────┘            │                       │
│                                         │                       │
│  Schedule(1:N per Professional)         │                       │
│  BlockedDate                            │                       │
│  Waitlist                               │                       │
└──────────────────────┘                  └──────────────────────┘
        │
        ▼
┌──────────────────────┐    ┌──────────────────────┐
│   PAYMENT CONTEXT    │    │ NOTIFICATION CONTEXT │
│                      │    │                       │
│  Payment             │    │  Template             │
│    ├── PaymentEvent  │    │  Notification         │
│    ├── Refund        │    │    (ref: booking,     │
│    └── (1:1 Booking) │    │     user, customer)   │
└──────────────────────┘    └──────────────────────┘

┌──────────────────────┐    ┌──────────────────────┐
│  MARKETING CONTEXT   │    │   AUDIT CONTEXT      │
│                      │    │                       │
│  Coupon              │    │  AuditLog             │
│  Campaign            │    │  LoginLog             │
│  LoyaltyPoints       │    │  SecurityEvent        │
│  LoyaltyTransaction  │    │                       │
│  Referral            │    │  (Todas as tabelas    │
│  Review              │    │   deste contexto são   │
│                      │    │   append-only)         │
└──────────────────────┘    └──────────────────────┘
```

---

## 2. Cardinalidades (Detalhamento)

### 2.1 Relacionamentos 1:1

| Entidade A | Entidade B | Descrição |
|-----------|-----------|-----------|
| Tenant | TenantSettings | Cada tenant tem exatamente 1 configuração |
| Tenant | TenantBranding | Cada tenant tem exatamente 1 branding |
| Tenant | SEOSettings | Cada tenant tem exatamente 1 config SEO |
| Booking | Payment | Cada booking tem no máximo 1 pagamento |
| Booking | Review | Cada booking tem no máximo 1 avaliação |
| Customer | CustomerPreference | Cada customer tem exatamente 1 preference |
| Customer | LoyaltyPoints | Cada customer tem exatamente 1 saldo de pontos |
| Professional | User | Profissional pode ter 1 user (login) opcional |
| User | Professional | User com role=professional pode ter 1 professional |

### 2.2 Relacionamentos 1:N

| Entidade A (1) | Entidade B (N) | Descrição |
|---------------|---------------|-----------|
| Tenant | User | Um tenant tem muitos usuários |
| Tenant | Customer | Um tenant tem muitos clientes |
| Tenant | Professional | Um tenant tem muitos profissionais |
| Tenant | Service | Um tenant tem muitos serviços |
| Tenant | Booking | Um tenant tem muitos agendamentos |
| Tenant | BusinessHours | Um tenant tem 7 registros (dias) |
| Tenant | Domain | Um tenant pode ter múltiplos domínios |
| Tenant | SocialMedia | Um tenant tem links para várias redes |
| Tenant | Media | Um tenant tem muitas mídias (galeria) |
| Tenant | Notification | Um tenant tem muitas notificações |
| Tenant | Payment | Um tenant tem muitos pagamentos |
| Tenant | Coupon | Um tenant tem muitos cupons |
| Tenant | Campaign | Um tenant tem muitas campanhas |
| Tenant | AuditLog | Um tenant tem muitos registros de auditoria |
| Tenant | GatewayConfig | Um tenant pode ter múltiplos gateways |
| Plan | Tenant | Um plano tem muitos tenants |
| Plan | Subscription | Um plano tem muitas assinaturas |
| ServiceCategory | Service | Uma categoria tem muitos serviços |
| Professional | Booking | Um profissional tem muitos agendamentos |
| Professional | Schedule | Um profissional tem até 7 schedules |
| Professional | BlockedDate | Um profissional tem muitas datas bloqueadas |
| Customer | Booking | Um cliente tem muitos agendamentos |
| Customer | Consent | Um cliente tem muitos registros de consentimento |
| Customer | Referral | Um cliente pode indicar muitas pessoas |
| Customer | Review | Um cliente pode fazer muitas avaliações |
| User | Session | Um user tem muitas sessões |
| User | RefreshToken | Um user tem muitos refresh tokens |
| User | PasswordReset | Um user tem muitos pedidos de reset |
| User | AuditLog | Um user pode gerar muitos logs |
| Booking | BookingService | Um booking tem 1+ serviços |
| Booking | BookingStatusLog | Um booking tem muitas transições de status |
| Payment | PaymentEvent | Um payment tem muitos eventos |
| Payment | Refund | Um payment pode ter múltiplos reembolsos |
| LoyaltyPoints | LoyaltyTransaction | Saldo tem muitas transações |
| NotificationTemplate | Campaign | Template usado em muitas campanhas |

### 2.3 Relacionamentos N:N

| Entidade A | Entidade B | Tabela Associativa | Descrição |
|-----------|-----------|-------------------|-----------|
| User | Role | user_roles | Usuário pode ter múltiplos papéis |
| Professional | Service | professional_services | Profissional realiza múltiplos serviços |
| Service | Booking | booking_services | Booking inclui múltiplos serviços |
| Booking | Coupon | booking_coupons | Booking pode usar múltiplos cupons |

---

## 3. Dependências

### 3.1 Dependências Fortes (FK NOT NULL)

```
Tenant ─────────────────────────────────────────────────────────────┐
  │ (quase todas as tabelas de negócio dependem de tenant)          │
  ▼                                                                 │
User, Customer, Professional, Service, Booking, Payment,             │
Schedule, BlockedDate, Media, Coupon, Campaign, AuditLog, ...        │
                                                                     │
Booking ───────────────────────────────────────────────────────────┐│
  ├── Professional (FK NOT NULL)                                    ││
  ├── Service (N:N via booking_services)                             ││
  └── date, start_time (obrigatórios)                                ││
                                                                     ││
Payment ───────────────────────────────────────────────────────────┐││
  └── Booking (FK NOT NULL)                                         │││
                                                                     │││
Professional ───────────────────────────────────────────────────────┘││
  └── Tenant (FK NOT NULL)                                           ││
                                                                     ││
Schedule ───────────────────────────────────────────────────────────┘│
  ├── Tenant (FK NOT NULL)                                            │
  └── Professional (FK NOT NULL)                                      │
                                                                      │
BookingService ──────────────────────────────────────────────────────┘
  ├── Booking (FK NOT NULL)
  └── Service (FK NOT NULL)
```

### 3.2 Dependências Fracas (FK NULLABLE)

| Entidade | FK Nullable | Quando é NULL |
|----------|-------------|---------------|
| Booking | customer_id | Guest (visitante sem cadastro) |
| Booking | created_by | Agendamento feito pelo site público |
| Customer | user_id | Cliente sem conta no sistema |
| Professional | user_id | Profissional sem login |
| BlockedDate | professional_id | Feriado/evento da barbearia toda |
| Waitlist | professional_id | "Qualquer profissional" |
| Notification | booking_id, user_id, customer_id | Depende do tipo de notificação |
| User | tenant_id | PlatformUser (super admin) |

---

## 4. Agregação vs. Composição

### Agregação (parte pode existir independente)

| Todo | Parte | Justificativa |
|------|-------|---------------|
| Tenant | Media | Mídia pode ser carregada antes de associada |
| Professional | Service | Serviço existe independente do profissional |
| Booking | Coupon | Cupom existe independente do booking |

### Composição (parte não existe sem o todo)

| Todo | Parte | Justificativa |
|------|-------|---------------|
| Booking | BookingService | Serviços do booking não existem sem o booking |
| Booking | BookingStatusLog | Log de status não existe sem o booking |
| Payment | PaymentEvent | Evento de pagamento não existe sem o payment |
| Payment | Refund | Reembolso não existe sem o payment |
| LoyaltyPoints | LoyaltyTransaction | Transação não existe sem o saldo |
| Customer | Consent | Consentimento vinculado ao ciclo de vida do customer |

---

## 5. Ordem de Criação (Dependências Topológicas)

Para criar registros na ordem correta e evitar violações de FK:

```
Nível 0 (sem dependências):
  Plan, FeatureFlag

Nível 1 (depende de Nível 0):
  Tenant (→ Plan)

Nível 2 (depende de Tenant):
  User, Customer, Professional, Service, ServiceCategory,
  BusinessHours, Domain, SocialMedia, GatewayConfig,
  TenantSettings, TenantBranding, SEOSettings

Nível 3 (depende de Nível 2):
  Schedule (→ Professional), BlockedDate (→ Professional),
  ProfessionalService (→ Professional + Service),
  UserRole (→ User + Role)

Nível 4 (depende de Nível 2 e 3):
  Booking (→ Customer, Professional), Waitlist

Nível 5 (depende de Nível 4):
  BookingService (→ Booking, Service),
  BookingStatusLog (→ Booking),
  Payment (→ Booking),
  Review (→ Booking, Customer, Professional)

Nível 6 (depende de Nível 5):
  PaymentEvent (→ Payment),
  Refund (→ Payment)

Nível 7 (transversais):
  Notification, AuditLog, LoginLog, SecurityEvent
```

---

## 6. Regras de Integridade Referencial

### ON DELETE

| Relacionamento | Regra | Justificativa |
|---------------|-------|---------------|
| Tenant → (tudo) | RESTRICT | Tenant nunca é deletado diretamente (soft delete) |
| Service → BookingService | RESTRICT | Booking referencia serviço (histórico) |
| Professional → Booking | RESTRICT | Booking referencia profissional (histórico) |
| Customer → Booking | SET NULL | Booking pode existir sem customer (guest) |
| User → AuditLog | SET NULL | Log permanece mesmo se user deletado |
| Booking → Payment | CASCADE | Se booking for hard-deleted (raro) |
| Payment → Refund | CASCADE | Refund sem payment não faz sentido |

### ON UPDATE

| Relacionamento | Regra |
|---------------|-------|
| Todos | CASCADE (UUIDs nunca mudam na prática) |

---

## 7. Diagrama de Módulos e Fluxo de Dados

```
┌──────────────────────────────────────────────────────────────────┐
│                     FLUXO DE DADOS                                │
│                                                                   │
│  ┌─────────┐     ┌─────────────┐     ┌─────────────┐            │
│  │ Tenant  │────►│ Scheduling  │────►│  Payment    │            │
│  │ Context │     │  Context    │     │  Context    │            │
│  └─────────┘     └──────┬──────┘     └─────────────┘            │
│                         │                                         │
│                         │ eventos                                 │
│                         ▼                                         │
│                  ┌─────────────┐                                  │
│                  │ Notification│                                  │
│                  │  Context    │                                  │
│                  └─────────────┘                                  │
│                         │                                         │
│                         ▼                                         │
│                  ┌─────────────┐     ┌─────────────┐            │
│                  │  Customer   │────►│  Marketing  │            │
│                  │  Context    │     │  Context    │            │
│                  └─────────────┘     └─────────────┘            │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                     AUDIT CONTEXT                             │ │
│  │  (Todos os contextos escrevem logs de auditoria)              │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 8. Polimorfismo e Herança

Não utilizamos herança de tabelas (PostgreSQL table inheritance) por questões de simplicidade e performance.

### Casos de "quase-herança" resolvidos com:

| Caso | Solução |
|------|---------|
| User pode ser admin, barbeiro, recepcionista | Coluna `role` (enum) + tabela `user_roles` (N:N) |
| Booking pode ter customer ou guest | `customer_id` NULLABLE + colunas `guest_name`, `guest_phone` |
| Media pode ser logo, banner, galeria, foto profissional | Coluna `type` (enum) |
| BlockedDate pode ser por profissional ou barbearia toda | `professional_id` NULLABLE |
| Notification pode ser de vários tipos | Coluna `event_type` + FKs opcionais |

---

> **Resumo:** O modelo de relacionamentos prioriza clareza e simplicidade. A maioria dos relacionamentos é 1:N com FK. Relacionamentos N:N são resolvidos com tabelas associativas explícitas. Composição é usada para entidades que não existem sem seu "parent" (ex: BookingService não existe sem Booking). A ordem de criação topológica garante que dependências de FK sejam sempre satisfeitas.
