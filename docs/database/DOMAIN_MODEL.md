# 01 — Domain Model (Modelagem de Domínio)

> Domain-Driven Design aplicado ao Barbershop SaaS.  
> Contextos delimitados, agregados, entidades, value objects.

---

## 1. Contextos Delimitados (Bounded Contexts)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         DOMÍNIOS DO SISTEMA                                │
│                                                                           │
│  ┌─────────────────────┐    ┌─────────────────────┐                      │
│  │  PLATFORM CONTEXT   │    │   TENANT CONTEXT     │                      │
│  │  (Super Admin)      │    │   (Configuração)     │                      │
│  │                     │    │                      │                      │
│  │  • Tenant (agreg.)  │    │  • TenantSettings    │                      │
│  │  • Plan             │    │  • TenantBranding    │                      │
│  │  • Subscription     │    │  • BusinessHours     │                      │
│  │  • PlatformUser     │    │  • SocialMedia       │                      │
│  │  • FeatureFlag      │    │  • Domain            │                      │
│  └─────────┬───────────┘    │  • Media (galeria)   │                      │
│            │                └──────────┬───────────┘                      │
│            │                           │                                   │
│            │          ┌────────────────┼────────────────┐                 │
│            │          │                │                │                 │
│  ┌─────────▼──────────▼──┐  ┌─────────▼──────────┐  ┌──▼──────────────┐ │
│  │   AUTH CONTEXT        │  │ SCHEDULING CONTEXT  │  │ CUSTOMER CONTEXT│ │
│  │                       │  │                    │  │                 │ │
│  │  • User (agreg.)      │  │ • Service          │  │ • Customer      │ │
│  │  • Role               │  │ • Professional     │  │ • Preference    │ │
│  │  • Permission         │  │ • Schedule         │  │ • Loyalty       │ │
│  │  • Session            │  │ • Booking (agreg.) │  │ • Referral      │ │
│  │  • RefreshToken       │  │ • BookingStatus    │  │ • Review        │ │
│  │  • PasswordReset      │  │ • Waitlist         │  │ • Consent       │ │
│  └───────────────────────┘  │ • BlockedDate      │  └────────────────┘ │
│                              └────────────────────┘                     │
│                                                                           │
│  ┌─────────────────────┐    ┌─────────────────────┐                      │
│  │  PAYMENT CONTEXT    │    │ NOTIFICATION CONTEXT│                      │
│  │                     │    │                     │                      │
│  │  • Payment (agreg.) │    │ • Notification      │                      │
│  │  • PaymentEvent     │    │ • Template          │                      │
│  │  • Refund           │    │ • DeliveryLog       │                      │
│  │  • GatewayConfig    │    │ • Channel           │                      │
│  │  • WebhookLog       │    │                     │                      │
│  └─────────────────────┘    └─────────────────────┘                      │
│                                                                           │
│  ┌─────────────────────┐    ┌─────────────────────┐                      │
│  │  MARKETING CONTEXT  │    │   AUDIT CONTEXT     │                      │
│  │                     │    │                     │                      │
│  │  • Coupon           │    │  • AuditLog         │                      │
│  │  • Campaign         │    │  • LoginLog         │                      │
│  │  • Promotion        │    │  • ChangeLog        │                      │
│  │  • LoyaltyProgram   │    │  • SecurityEvent    │                      │
│  └─────────────────────┘    └─────────────────────┘                      │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Agregados (Aggregate Roots)

Um agregado é um cluster de entidades e value objects que são tratados como uma unidade. O **aggregate root** é a única entidade que referências externas podem acessar.

### 2.1 Agregado: Tenant

```
┌──────────────────────────────────────────────────────────────────┐
│  AGGREGATE ROOT: Tenant                                          │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Tenant (AR)                                                  │ │
│  │   id, subdomain, name, status, plan_id, created_at           │ │
│  └─────────────────────────────────────────────────────────────┘ │
│           │                                                       │
│           ├── TenantSettings (1:1)                                │
│           │     timezone, language, currency, notification_prefs  │
│           │                                                       │
│           ├── TenantBranding (1:1)                                │
│           │     logo_url, banner_url, primary_color,              │
│           │     secondary_color, heading_font, body_font          │
│           │                                                       │
│           ├── BusinessHours (1:N)                                 │
│           │     day_of_week, open_time, close_time, is_closed     │
│           │                                                       │
│           ├── SocialMedia (1:N)                                   │
│           │     platform, url                                     │
│           │                                                       │
│           ├── Domain (1:N)                                        │
│           │     domain_name, is_primary, verified_at              │
│           │                                                       │
│           └── Media[] (1:N — galeria, fotos)                      │
│                 file_url, type, title, order                     │
└──────────────────────────────────────────────────────────────────┘

Regras de negócio:
- Subdomínio é único globalmente
- Tenant tem exatamente 1 plano ativo
- BusinessHours define slots disponíveis
- Tenant não pode acessar dados de outro tenant
```

### 2.2 Agregado: Booking

```
┌──────────────────────────────────────────────────────────────────┐
│  AGGREGATE ROOT: Booking                                         │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Booking (AR)                                                 │ │
│  │   id, tenant_id, customer_id, professional_id, service_id,  │ │
│  │   date, start_time, end_time, status, notes, total_amount   │ │
│  └─────────────────────────────────────────────────────────────┘ │
│           │                                                       │
│           ├── BookingService (1:N — múltiplos serviços)           │
│           │     service_id, price, duration                       │
│           │                                                       │
│           ├── BookingStatusLog (1:N — histórico de status)        │
│           │     from_status, to_status, changed_by, timestamp    │
│           │                                                       │
│           ├── Payment (1:1 — pagamento associado)                 │
│           │     payment_id, gateway, status, amount              │
│           │                                                       │
│           └── Review (1:1 — avaliação pós-atendimento)            │
│                 rating, comment, tags                             │
└──────────────────────────────────────────────────────────────────┘

Regras de negócio:
- Não pode haver double-booking (mesmo profissional, data, horário)
- Duração calculada pela soma dos serviços
- Status segue máquina de estados definida
- Cliente pode cancelar até 2h antes (configurável)
- Agendamento como visitante: customer_id opcional (guest info no booking)
```

### 2.3 Agregado: Payment

```
┌──────────────────────────────────────────────────────────────────┐
│  AGGREGATE ROOT: Payment                                         │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Payment (AR)                                                 │ │
│  │   id, tenant_id, booking_id, gateway_payment_id,            │ │
│  │   gateway, amount, currency, status, paid_at                │ │
│  └─────────────────────────────────────────────────────────────┘ │
│           │                                                       │
│           ├── PaymentEvent (1:N — event sourcing)                 │
│           │     event_type, gateway_raw_data (JSONB), timestamp  │
│           │                                                       │
│           └── Refund (1:N)                                        │
│                 amount, reason, gateway_refund_id, status        │
└──────────────────────────────────────────────────────────────────┘

Regras de negócio:
- NUNCA armazenar dados de cartão (PCI-DSS compliance)
- Status gerenciado via webhooks do gateway
- Refund só pode ser total ou parcial, nunca exceder valor pago
- Event sourcing para audit trail completo
```

### 2.4 Agregado: User

```
┌──────────────────────────────────────────────────────────────────┐
│  AGGREGATE ROOT: User (dentro do tenant)                         │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ User (AR)                                                    │ │
│  │   id, tenant_id, email, password_hash, name, phone,         │ │
│  │   role, is_active, last_login_at                            │ │
│  └─────────────────────────────────────────────────────────────┘ │
│           │                                                       │
│           ├── Role (N:N via user_roles)                           │
│           │     name, permissions[] (JSONB)                       │
│           │                                                       │
│           ├── Session (1:N)                                       │
│           │     token_hash, expires_at, ip, user_agent           │
│           │                                                       │
│           ├── RefreshToken (1:N)                                  │
│           │     token_hash, family_id, expires_at, is_revoked    │
│           │                                                       │
│           └── PasswordReset (1:N)                                 │
│                 token_hash, expires_at, used_at                  │
└──────────────────────────────────────────────────────────────────┘

Regras de negócio:
- Email único por tenant
- Senha: bcrypt hash, cost ≥ 12
- Refresh token: rotação a cada uso, família invalida em reuso
- Lockout: 5 tentativas → 15 min bloqueio
```

---

## 3. Value Objects

Objetos imutáveis definidos por seus atributos, sem identidade própria.

| Value Object | Atributos | Usado Em |
|-------------|-----------|----------|
| `Money` | amount (integer, centavos), currency (enum BRL) | Payment, Booking, Service |
| `TimeSlot` | start_time (TIME), end_time (TIME) | Schedule, Booking, BusinessHours |
| `PhoneNumber` | country_code, area_code, number | Customer, User, Tenant |
| `Address` | street, number, neighborhood, city, state, zip_code, lat, lng | Tenant |
| `Color` | hex (string, 6 chars), opacity (0-1) | TenantBranding |
| `DateRange` | start_date, end_date | Promotion, BlockedDate, Campaign |
| `Rating` | score (1-5), comment (text), tags (string[]) | Review |
| `GeoLocation` | latitude, longitude | Tenant (endereço) |
| `Duration` | total_minutes (integer) | Service, Booking |

---

## 4. Enums (Tipos de Domínio)

### booking_status

| Valor | Descrição | Transições Válidas |
|-------|-----------|-------------------|
| `pending` | Aguardando pagamento/confirmação | → confirmed, cancelled, expired |
| `confirmed` | Confirmado (pagamento ok ou sem pagamento) | → checked_in, cancelled, no_show |
| `checked_in` | Cliente chegou | → in_progress |
| `in_progress` | Em atendimento | → completed |
| `completed` | Atendimento concluído | → reviewed (final) |
| `cancelled` | Cancelado (cliente ou admin) | final |
| `no_show` | Não compareceu | final |
| `expired` | Expirado (pagamento não concluído) | final |

### payment_status

| Valor | Descrição |
|-------|-----------|
| `pending` | Aguardando processamento |
| `processing` | Gateway está processando |
| `paid` | Pago com sucesso |
| `failed` | Falha no pagamento |
| `refunded` | Totalmente reembolsado |
| `partially_refunded` | Parcialmente reembolsado |
| `expired` | Tempo de pagamento expirado |

### tenant_status

| Valor | Descrição |
|-------|-----------|
| `trial` | Período de teste (14 dias) |
| `active` | Assinatura ativa |
| `past_due` | Pagamento atrasado |
| `suspended` | Suspenso por falta de pagamento |
| `cancelled` | Cancelado voluntariamente |
| `deleted` | Excluído (dados anonimizados) |

### user_role

| Valor | Descrição |
|-------|-----------|
| `super_admin` | Acesso total à plataforma |
| `admin` | Dono/administrador do tenant |
| `manager` | Gerente do tenant |
| `receptionist` | Recepcionista |
| `professional` | Barbeiro/profissional |
| `customer` | Cliente final |

---

## 5. Máquinas de Estado

### Booking — Ciclo de Vida

```
                    ┌──────────┐
                    │ pending  │
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
        ┌─────────┐ ┌─────────┐ ┌─────────┐
        │confirmed│ │cancelled│ │ expired │
        └────┬────┘ └─────────┘ └─────────┘
             │
        ┌────┴────┐
        ▼         ▼
  ┌──────────┐ ┌─────────┐
  │checked_in│ │no_show  │
  └────┬─────┘ └─────────┘
       │
       ▼
  ┌──────────┐
  │in_progress│
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │completed │
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │ reviewed │ (final)
  └──────────┘
```

### Payment — Ciclo de Vida

```
  ┌──────────┐
  │ pending  │
  └────┬─────┘
       │
       ▼
  ┌────────────┐
  │ processing │
  └──┬────┬────┘
     │    │
     ▼    ▼
┌──────┐ ┌────────┐
│ paid │ │ failed │
└──┬───┘ └────────┘
   │
   ├──────────┐
   ▼          ▼
┌───────────┐ ┌──────────────────────┐
│ refunded  │ │ partially_refunded   │
└───────────┘ └──────────────────────┘
```

### Tenant — Ciclo de Vida

```
  ┌──────────┐
  │  trial   │ (14 dias)
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │  active  │
  └──┬───┬───┘
     │   │
     ▼   ▼
┌──────────┐ ┌───────────┐
│ past_due │ │ cancelled │
└────┬─────┘ └─────┬─────┘
     │             │
     ▼             ▼
┌───────────┐ ┌──────────┐
│ suspended │ │ deleted  │
└───────────┘ └──────────┘
     │
     ├── Pagamento regularizado → active
     └── 90 dias sem pagamento → deleted
```

---

## 6. Regras de Domínio (Domain Rules)

### Scheduling

- **DR-01:** Um profissional não pode ter 2 agendamentos no mesmo horário
- **DR-02:** Duração do booking = soma das durações dos serviços
- **DR-03:** Cliente só pode agendar em horário de funcionamento
- **DR-04:** Cliente pode cancelar até X horas antes (configurável por tenant)
- **DR-05:** Agendamento sem pagamento expira em 15 minutos (tempo de reserva)

### Payment

- **DR-06:** Nunca armazenar dados de cartão
- **DR-07:** Pagamento de sinal é obrigatório para confirmar booking (V1+)
- **DR-08:** Sinal é abatido do valor total do serviço
- **DR-09:** Reembolso do sinal em cancelamento dentro do prazo

### Tenant

- **DR-10:** Trial de 14 dias com todas as funcionalidades do plano escolhido
- **DR-11:** Após trial, tenant é suspenso se não assinar
- **DR-12:** Tenant suspenso: site pausado (página "volte logo"), admin acessível
- **DR-13:** Dados do tenant preservados por 90 dias após cancelamento

### Customer

- **DR-14:** Cliente pode agendar sem cadastro (guest)
- **DR-15:** Telefone é o identificador único do cliente por tenant
- **DR-16:** Cliente pode solicitar exclusão de dados (LGPD — soft delete → hard delete 30d)

---

## 7. Eventos de Domínio

Eventos que disparam ações em outros contextos:

| Evento | Origem | Consumidores |
|--------|--------|-------------|
| `booking.created` | Scheduling | Notification (confirmação), CRM (histórico) |
| `booking.cancelled` | Scheduling | Notification, Payment (reembolso se aplicável) |
| `booking.completed` | Scheduling | CRM (histórico), Loyalty (pontos), Notification (avaliação) |
| `payment.succeeded` | Payment | Scheduling (confirma booking), Notification |
| `payment.refunded` | Payment | Scheduling (cancela booking), Notification |
| `tenant.created` | Platform | Tenant (setup inicial) |
| `tenant.suspended` | Platform | Tenant (pausa site) |
| `customer.registered` | Customer | CRM, Notification (boas-vindas) |
| `review.created` | Customer | Professional (atualiza rating), Tenant (dashboard) |

---

## 8. Diagrama de Contextos (Visão Macro)

```
                          ┌───────────────┐
                          │   Platform    │
                          │   Context     │
                          └───────┬───────┘
                                  │ manages
                                  ▼
┌──────────────┐    ┌────────────────────────────┐    ┌──────────────┐
│    Auth      │◄───│        Tenant              │───►│  Marketing   │
│   Context    │    │        Context             │    │   Context    │
└──────────────┘    └────────┬───────────────────┘    └──────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌────────────┐ ┌──────────────┐ ┌──────────────┐
     │ Scheduling │ │   Payment    │ │ Notification │
     │  Context   │ │   Context    │ │   Context    │
     └─────┬──────┘ └──────────────┘ └──────────────┘
           │
           ▼
     ┌────────────┐
     │  Customer  │
     │  Context   │
     └────────────┘

     (Todos os contextos de negócio dependem de Tenant)
```

---

> **Resumo:** O Domain Model organiza o sistema em 9 contextos delimitados. Cada contexto tem seus agregados, value objects, enums e regras de negócio. A comunicação entre contextos é feita via eventos de domínio (assíncrono) ou via API (síncrono). Os agregados garantem consistência transacional dentro de cada contexto.
