# 02 — Event Bus & Domain Events

> Arquitetura de eventos do sistema.  
> Event-driven communication entre contextos delimitados.

---

## 1. Filosofia

> "Todo acontecimento relevante no sistema é um evento. Eventos são imutáveis, versionados e carregam apenas os dados necessários para os consumidores."

### Princípios

1. **Imutável:** Um evento publicado nunca é alterado.
2. **Passado:** Nome do evento no passado: `booking.created`, não `booking.create`.
3. **Autossuficiente:** O evento carrega os dados que os consumidores precisam.
4. **Desacoplado:** O produtor não sabe quem consome.
5. **Assíncrono:** Consumidores processam em background (não bloqueiam o produtor).

---

## 2. Arquitetura do Event Bus

```
┌──────────────────────────────────────────────────────────────────┐
│                         EVENT BUS                                 │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    PRODUCERS (Emitem Eventos)                │ │
│  │                                                              │ │
│  │  Scheduling Service  ──► booking.created                    │ │
│  │  Scheduling Service  ──► booking.cancelled                  │ │
│  │  Scheduling Service  ──► booking.completed                  │ │
│  │  Payment Service     ──► payment.succeeded                  │ │
│  │  Payment Service     ──► payment.refunded                   │ │
│  │  Customer Service    ──► customer.registered                 │ │
│  │  Review Service      ──► review.created                     │ │
│  │  Tenant Service      ──► tenant.activated                   │ │
│  │  Tenant Service      ──► tenant.suspended                   │ │
│  │  Tenant Service      ──► branding.updated                   │ │
│  └──────────────────────────────┬──────────────────────────────┘ │
│                                 │                                  │
│  ┌──────────────────────────────▼──────────────────────────────┐ │
│  │              MESSAGE BROKER (Redis Streams)                 │ │
│  │                                                              │ │
│  │  Stream: events                                              │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │ { "type": "booking.created", "data": {...}, ... }      │ │ │
│  │  │ { "type": "payment.succeeded", "data": {...}, ... }    │ │ │
│  │  │ { "type": "customer.registered", "data": {...}, ... }  │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────┬──────────────────────────────┘ │
│                                 │                                  │
│  ┌──────────────────────────────▼──────────────────────────────┐ │
│  │                  CONSUMERS (Reagem a Eventos)               │ │
│  │                                                              │ │
│  │  ┌──────────────────┐  ┌──────────────────┐                 │ │
│  │  │ Notification     │  │ CRM Service      │                 │ │
│  │  │ Service          │  │                  │                 │ │
│  │  │ booking.created  │  │ booking.completed│                 │ │
│  │  │ → WhatsApp       │  │ → update history │                 │ │
│  │  │ → Email          │  │ → update counters│                 │ │
│  │  │ → Push           │  └──────────────────┘                 │ │
│  │  └──────────────────┘                                       │ │
│  │  ┌──────────────────┐  ┌──────────────────┐                 │ │
│  │  │ Analytics        │  │ Webhook          │                 │ │
│  │  │ Service          │  │ Dispatcher       │                 │ │
│  │  │ *.* → metrics    │  │ *.* → outbound   │                 │ │
│  │  └──────────────────┘  │ webhooks         │                 │ │
│  │                         └──────────────────┘                 │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Schema do Evento

### Estrutura Padrão

```json
{
  "id": "evt_abc123def456",
  "type": "booking.created",
  "version": "1.0",
  "timestamp": "2026-07-20T14:30:00.000Z",
  "tenant_id": "t_001",
  "correlation_id": "req_xyz789",
  "causation_id": null,
  "data": {
    "booking_id": "b_456",
    "customer_id": "c_123",
    "customer_name": "João Silva",
    "professional_id": "p_789",
    "professional_name": "Marcos",
    "service_id": "s_001",
    "service_name": "Corte",
    "service_price": 4500,
    "date": "2026-07-25",
    "start_time": "14:30",
    "end_time": "15:00"
  },
  "metadata": {
    "source": "public_site",
    "environment": "production"
  }
}
```

### Campos Obrigatórios

| Campo | Descrição |
|-------|-----------|
| `id` | UUID v7 — identificador único do evento |
| `type` | Nome do evento (snake_case, passado) |
| `version` | Versão do schema do evento (SemVer) |
| `timestamp` | ISO 8601 UTC |
| `tenant_id` | Tenant que originou o evento |
| `correlation_id` | request_id original (para tracing) |
| `data` | Payload específico do evento |

---

## 4. Catálogo de Eventos

### Scheduling Events

| Evento | Descrição | Payload Principal |
|--------|-----------|-------------------|
| `booking.created` | Novo agendamento criado | booking_id, customer, professional, service, date, time |
| `booking.confirmed` | Agendamento confirmado (pós pagamento) | booking_id, payment_id |
| `booking.cancelled` | Agendamento cancelado | booking_id, reason, cancelled_by |
| `booking.rescheduled` | Agendamento reagendado | booking_id, old_date, old_time, new_date, new_time |
| `booking.checked_in` | Cliente chegou | booking_id, checked_in_at |
| `booking.completed` | Atendimento concluído | booking_id, completed_at |
| `booking.no_show` | Cliente não compareceu | booking_id |
| `booking.reminder_sent` | Lembrete enviado | booking_id, channel |

### Payment Events

| Evento | Descrição | Payload Principal |
|--------|-----------|-------------------|
| `payment.created` | Intenção de pagamento criada | payment_id, booking_id, amount, gateway |
| `payment.succeeded` | Pagamento aprovado | payment_id, booking_id, paid_at |
| `payment.failed` | Pagamento recusado | payment_id, booking_id, reason |
| `payment.refunded` | Reembolso processado | payment_id, booking_id, refund_amount |
| `payment.expired` | Pagamento expirado | payment_id, booking_id |

### Customer Events

| Evento | Descrição | Payload Principal |
|--------|-----------|-------------------|
| `customer.registered` | Cliente cadastrado | customer_id, name, phone |
| `customer.updated` | Dados do cliente alterados | customer_id, changed_fields |
| `customer.deleted` | Cliente excluído (LGPD) | customer_id, deleted_at |
| `review.created` | Avaliação recebida | review_id, booking_id, rating, comment |
| `loyalty.points_earned` | Pontos ganhos | customer_id, points, source |
| `loyalty.points_redeemed` | Pontos resgatados | customer_id, points, reward |
| `referral.converted` | Indicação convertida | referrer_id, referred_name |

### Tenant Events

| Evento | Descrição | Payload Principal |
|--------|-----------|-------------------|
| `tenant.created` | Nova empresa cadastrada | tenant_id, plan_id |
| `tenant.activated` | Empresa ativada | tenant_id, plan_id |
| `tenant.suspended` | Empresa suspensa | tenant_id, reason |
| `tenant.cancelled` | Empresa cancelou | tenant_id |
| `branding.updated` | Tema/site alterado | tenant_id, changed_fields |

### Auth Events

| Evento | Descrição | Payload Principal |
|--------|-----------|-------------------|
| `user.logged_in` | Login bem-sucedido | user_id, ip, tenant_id |
| `user.logged_out` | Logout | user_id |
| `user.password_changed` | Senha alterada | user_id |
| `user.invited` | Convite enviado | email, role, invited_by |

---

## 5. Padrão de Consumo

### Consumer Group (Redis Streams)

```
┌──────────────────────────────────────────────────────────────────┐
│              CONSUMER GROUPS                                      │
│                                                                   │
│  Stream: events                                                   │
│                                                                   │
│  Group: notification-service                                      │
│  ├── Consumer: whatsapp-worker-1                                  │
│  ├── Consumer: whatsapp-worker-2  (horizontal scaling)           │
│  ├── Consumer: email-worker-1                                     │
│  └── Consumer: push-worker-1                                      │
│                                                                   │
│  Group: crm-service                                               │
│  ├── Consumer: history-worker-1                                   │
│  └── Consumer: counter-worker-1                                   │
│                                                                   │
│  Group: webhook-dispatcher                                        │
│  └── Consumer: outbound-worker-1                                  │
│                                                                   │
│  Cada grupo mantém seu próprio offset.                            │
│  Cada consumidor processa eventos de forma independente.          │
│  Se um consumidor falha, outro do mesmo grupo assume (redelivery).│
└──────────────────────────────────────────────────────────────────┘
```

### Retry e Dead Letter Queue

```
┌──────────────────────────────────────────────────────────────────┐
│              EVENT PROCESSING LIFECYCLE                            │
│                                                                   │
│  Evento recebido do stream                                        │
│      │                                                            │
│      ▼                                                            │
│  ┌─────────────┐                                                  │
│  │ Processar   │ ← Consumidor tenta processar                    │
│  └──┬──────┬───┘                                                  │
│     │      │                                                      │
│     ▼      ▼                                                      │
│   ✅ OK   ❌ Falha                                                 │
│     │      │                                                      │
│     │      ▼                                                      │
│     │  ┌─────────────┐                                            │
│     │  │ Retry Count │ < 3? → Reenfileirar com backoff           │
│     │  │    < 3      │                                            │
│     │  └──────┬──────┘                                            │
│     │         │                                                    │
│     │         ▼                                                    │
│     │  ┌─────────────┐                                            │
│     │  │ Retry Count │ ≥ 3? → Dead Letter Queue                  │
│     │  │    ≥ 3      │         (inspeção manual)                  │
│     │  └─────────────┘                                            │
│     │                                                              │
│     ▼                                                              │
│  ✅ ACK (confirma processamento)                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. DLQ (Dead Letter Queue)

### Estrutura

```
Stream: events:dlq

Mensagem na DLQ carrega:
{
  "original_event": { ... },       // Evento original
  "error": "WhatsApp API timeout", // Motivo da falha
  "retry_count": 3,                // Tentativas esgotadas
  "consumer": "whatsapp-worker-1", // Quem tentou processar
  "failed_at": "2026-07-20T14:35:00Z",
  "stack_trace": "..."
}
```

### Operação

1. DLQ é monitorada via Grafana (dashboard dedicado)
2. Alerta quando DLQ acumula > 100 mensagens
3. Inspeção manual via painel admin (Super Admin)
4. Ações possíveis: Replay (reenfileirar), Discard, Fix + Replay

---

## 7. Tracing (Correlation)

Todo evento carrega `correlation_id` (request_id original) e `causation_id`:

```
Request: POST /api/v1/bookings
  → correlation_id: req_abc

Evento: booking.created
  → correlation_id: req_abc
  → id: evt_001

Evento: notification.sent (causado por booking.created)
  → correlation_id: req_abc (mesmo request original)
  → causation_id: evt_001 (evento que causou este)
  → id: evt_002

Isso permite rastrear: request → booking → notification
```

---

## 8. Versionamento de Eventos

### Schema Registry (Conceitual)

```
Cada evento tem versão no campo "version":

booking.created:
  v1.0: { booking_id, customer_name, professional_name, ... }
  v2.0: { ...v1.0 + customer_phone, professional_rating }
  v3.0: { ...v2.0 + promotion_code }

Regras:
- Adicionar campo → MINOR version (1.0 → 1.1)
- Remover/renomear campo → MAJOR version (1.x → 2.0)
- Consumidores devem ignorar campos desconhecidos (forward-compat)
- Consumidores devem tratar campos ausentes com default (backward-compat)
```

---

> **Resumo:** O Event Bus é a espinha dorsal da comunicação assíncrona entre contextos. Eventos são imutáveis, versionados e autossuficientes. O Redis Streams serve como broker com consumer groups para escalabilidade horizontal. DLQ garante que nenhum evento seja perdido sem rastro. Correlation ID permite tracing ponta-a-ponta.
