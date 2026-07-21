# 🔌 Barbershop SaaS — Arquitetura de Integrações

> **Versão:** 1.0.0  
> **Data:** Julho 2026  
> **Princípio:** Todo serviço externo é um módulo plugável. Zero acoplamento direto.  
> **Referências:** Stripe Connect · Shopify App Bridge · Zapier Platform · Slack API

---

## Índice

| # | Documento | Descrição |
|---|-----------|-----------|
| — | `INTEGRATIONS.md` | Hub de Integrações, Gateway, estratégia geral |
| 01 | `WEBHOOKS.md` | Padrão de Webhooks, assinatura, idempotência, retry |
| 02 | `EVENTS.md` | Event Bus, domain events, fila, DLQ |
| 03 | `THIRD_PARTY.md` | Catálogo de serviços, interfaces, contratos |
| 04 | `API_PUBLIC.md` | API Pública, OAuth, rate limit, versionamento |

---

## 1. Filosofia do Integration Hub

> "Toda integração externa é um adaptador plugável. O sistema NUNCA conhece o serviço concreto — apenas a interface."

### Regras de Ouro

1. **Dependency Inversion:** O domínio define a interface (port). O adaptador implementa.
2. **Zero Acoplamento:** Nenhum módulo de negócio importa SDK de terceiros diretamente.
3. **Substituível:** Trocar Stripe por PagSeguro = implementar nova classe, não reescrever regras.
4. **Testável:** Toda integração pode ser mockada em testes — sem dependências reais.
5. **Observável:** Toda chamada externa gera log, métrica e trace.

---

## 2. Arquitetura do Integration Hub

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        INTEGRATION HUB                                    │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                    APPLICATION LAYER (Use Cases)                     │ │
│  │  BookingUseCase, PaymentUseCase, NotificationUseCase               │ │
│  │  ↓ (depende de interfaces/ports)                                    │ │
│  └───────────────────────────────┬─────────────────────────────────────┘ │
│                                  │                                        │
│  ┌───────────────────────────────▼─────────────────────────────────────┐ │
│  │                    DOMAIN LAYER (Interfaces/Ports)                   │ │
│  │                                                                      │ │
│  │  PaymentGateway (interface)        NotificationSender (interface)    │ │
│  │  ├── create_payment_intent()       ├── send()                        │ │
│  │  ├── process_webhook()            ├── send_template()               │ │
│  │  ├── refund()                     └── get_status()                  │ │
│  │  └── get_status()                                                   │ │
│  │                                                                      │ │
│  │  StorageProvider (interface)       CalendarProvider (interface)      │ │
│  │  ├── upload()                      ├── create_event()                │ │
│  │  ├── get_url()                    ├── update_event()               │ │
│  │  └── delete()                     └── delete_event()                │ │
│  └───────────────────────────────┬─────────────────────────────────────┘ │
│                                  │                                        │
│  ┌───────────────────────────────▼─────────────────────────────────────┐ │
│  │               INFRASTRUCTURE LAYER (Adapters/Implementations)       │ │
│  │                                                                      │ │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐       │ │
│  │  │ Stripe     │ │ MercadoPago│ │ Twilio     │ │ AWS SES    │       │ │
│  │  │ Adapter    │ │ Adapter    │ │ Adapter    │ │ Adapter    │       │ │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘       │ │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐       │ │
│  │  │ WhatsApp   │ │ Cloudflare │ │ Google     │ │ n8n        │       │ │
│  │  │ Adapter    │ │ R2 Adapter │ │ Cal Adptr  │ │ Adapter    │       │ │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘       │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                    INTEGRATION INFRASTRUCTURE                         │ │
│  │                                                                      │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │  │ Circuit  │  │  Retry   │  │   DLQ    │  │ Metrics  │            │ │
│  │  │ Breaker  │  │  Engine  │  │ (Redis)  │  │Collector │            │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │  │Webhook   │  │  Secret  │  │  Audit   │  │  Health  │            │ │
│  │  │Validator │  │  Vault   │  │  Logger  │  │  Checker │            │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Padrão de Adapter (Interface + Implementação)

### Estrutura de Diretórios (por serviço)

```
backend/src/infrastructure/integrations/
├── __init__.py
├── base.py                          # Interfaces base + infra compartilhada
│
├── payment/                         # Payment Gateway
│   ├── __init__.py
│   ├── interface.py                 # PaymentGateway (abstract)
│   ├── adapters/
│   │   ├── stripe_adapter.py        # StripeAdapter(PaymentGateway)
│   │   ├── mercadopago_adapter.py   # MercadoPagoAdapter(PaymentGateway)
│   │   ├── pagseguro_adapter.py     # PagSeguroAdapter(PaymentGateway)
│   │   └── asaas_adapter.py         # AsaasAdapter(PaymentGateway)
│   ├── webhook.py                   # Webhook router + validator
│   └── registry.py                  # Gateway registry (factory)
│
├── notification/                    # Multi-channel Notifications
│   ├── __init__.py
│   ├── interface.py                 # NotificationSender (abstract)
│   ├── adapters/
│   │   ├── whatsapp_adapter.py      # WhatsApp Cloud API
│   │   ├── email_ses_adapter.py     # AWS SES
│   │   ├── email_resend_adapter.py  # Resend
│   │   └── sms_twilio_adapter.py    # Twilio SMS
│   └── dispatch.py                  # Router: channel → adapter
│
├── storage/                         # File Storage
│   ├── __init__.py
│   ├── interface.py                 # StorageProvider (abstract)
│   ├── adapters/
│   │   ├── s3_adapter.py            # AWS S3
│   │   ├── r2_adapter.py            # Cloudflare R2
│   │   └── local_adapter.py         # Local (dev/test)
│   └── processor.py                 # Image processing pipeline
│
├── calendar/                        # Google Calendar
│   ├── __init__.py
│   ├── interface.py                 # CalendarProvider
│   └── adapters/
│       └── google_calendar_adapter.py
│
├── analytics/                       # Analytics & Tracking
│   ├── __init__.py
│   ├── interface.py                 # AnalyticsProvider
│   └── adapters/
│       ├── google_analytics_adapter.py
│       └── meta_pixel_adapter.py
│
└── automation/                      # Automation (n8n, Zapier, Make)
    ├── __init__.py
    ├── interface.py                 # AutomationProvider
    └── adapters/
        └── webhook_outbound_adapter.py
```

---

## 4. Integration Registry (Factory Pattern)

Cada categoria de integração tem um **Registry** que mapeia provedor → classe concreta.

```
┌──────────────────────────────────────────────────────────────────┐
│                    PAYMENT GATEWAY REGISTRY                       │
│                                                                   │
│  Config (por tenant):                                             │
│  {                                                                │
│    "tenant_id": "t_001",                                          │
│    "gateway": "stripe",                                           │
│    "api_key_encrypted": "aes256...",                              │
│    "webhook_secret_encrypted": "aes256..."                        │
│  }                                                                │
│                                                                   │
│  Registry resolve em runtime:                                     │
│  registry.get("stripe") → StripeAdapter(api_key, webhook_secret)  │
│  registry.get("mercadopago") → MercadoPagoAdapter(...)            │
│                                                                   │
│  Uso no código:                                                   │
│  gateway = registry.get_for_tenant(tenant_id)                     │
│  result = await gateway.create_payment_intent(1000, "BRL")       │
│                                                                   │
│  Para trocar de gateway: alterar 1 registro no banco.             │
│  Zero mudança de código.                                          │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Circuit Breaker & Retry

### Arquitetura de Resiliência

```
┌──────────────────────────────────────────────────────────────────┐
│              RESILIENCE LAYER                                     │
│                                                                   │
│  Chamada externa                                                  │
│      │                                                            │
│      ▼                                                            │
│  ┌─────────────┐                                                  │
│  │ Circuit     │ ← Aberto após 5 falhas consecutivas             │
│  │ Breaker     │ ← Half-open: testa após 30s                     │
│  └──────┬──────┘ ← Fechado: após 2 sucessos                      │
│         │                                                         │
│         ▼                                                         │
│  ┌─────────────┐                                                  │
│  │ Retry       │ ← 3 tentativas                                  │
│  │ Engine      │ ← Backoff: 1s, 2s, 4s (+ jitter)               │
│  └──────┬──────┘ ← Apenas operações idempotentes                 │
│         │                                                         │
│         ├─── Sucesso → ✅ Retorna resultado                       │
│         │                                                         │
│         └─── Todas falhas → ┌─────────────┐                      │
│                              │ Dead Letter │ ← Inspeção manual    │
│                              │ Queue (DLQ) │ ← Replay possível    │
│                              └─────────────┘                      │
└──────────────────────────────────────────────────────────────────┘
```

### Configuração por Serviço

| Serviço | Circuit Breaker | Retry Max | Backoff | DLQ |
|---------|:--------------:|:---------:|---------|:---:|
| Pagamento (create) | 5 falhas / 30s | 0 | — | ✅ |
| Pagamento (webhook) | — | 3 | 1s, 5s, 15s | ✅ |
| WhatsApp (send) | 5 falhas / 60s | 3 | 1min, 5min, 15min | ✅ |
| E-mail (send) | 5 falhas / 30s | 3 | 30s, 2min, 10min | ✅ |
| SMS (send) | 5 falhas / 30s | 2 | 30s, 5min | ✅ |
| Storage (upload) | 3 falhas / 30s | 2 | 5s, 30s | ✅ |
| Calendar (API) | 3 falhas / 60s | 2 | 10s, 60s | ❌ |
| Analytics (track) | 3 falhas / 60s | 0 | — | ❌ |

---

## 6. Estratégia de Segurança para Integrações

### Secrets Management

```
┌──────────────────────────────────────────────────────────────────┐
│                    SECRETS VAULT                                  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Source: Environment Variables (dev) / Vault (prod)           │ │
│  │                                                              │ │
│  │ Secrets NUNCA em:                                            │ │
│  │  ✗ Código fonte                                             │ │
│  │  ✗ Git                                                     │ │
│  │  ✗ Logs                                                    │ │
│  │  ✗ Config files                                            │ │
│  │                                                              │ │
│  │ Storage:                                                     │ │
│  │  Banco: tenant_gateway_configs (api_key_encrypted)           │ │
│  │  Criptografia: AES-256-GCM                                   │ │
│  │  Rotação: 90 dias (manual) / automática (Vault)             │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### Webhook Security

| Camada | Mecanismo |
|--------|-----------|
| **Transporte** | TLS 1.3 obrigatório |
| **Autenticidade** | HMAC-SHA256 (webhook signature header) |
| **Replay Attack** | Timestamp check (±5 min tolerance) |
| **Idempotência** | `idempotency_key` no payload |
| **IP Allowlist** | Restrito aos IPs do gateway (produção) |
| **Rate Limit** | Max 100 webhooks/min por gateway |

---

## 7. Estratégia de Logs e Métricas

### Logs

```
Toda chamada externa gera:
{
  "timestamp": "2026-07-20T14:30:00Z",
  "integration": "payment",
  "provider": "stripe",
  "operation": "create_payment_intent",
  "duration_ms": 245,
  "status": "success",
  "request_id": "req_abc",
  "tenant_id": "t_001",
  "error": null,
  "retry_count": 0
}
```

### Métricas (Prometheus)

| Métrica | Labels |
|---------|--------|
| `integration_requests_total` | provider, operation, status |
| `integration_request_duration_seconds` | provider, operation |
| `integration_circuit_breaker_state` | provider (0=closed, 1=half_open, 2=open) |
| `integration_retry_total` | provider, operation |
| `integration_dlq_size` | provider |
| `webhook_received_total` | gateway, event_type |

### Alertas

| Alerta | Condição |
|--------|----------|
| Circuit breaker aberto | `circuit_breaker_state == 2` por > 1 min |
| DLQ acumulando | `dlq_size > 100` |
| Webhook falhando | `webhook_failure_rate > 10%` |
| Latência elevada | `p95 > 5s` para qualquer provider |

---

## 8. Versionamento de Integrações

Cada adapter segue versionamento semântico da API do provedor:

```
Adapter: StripeAdapter
  ├── v1: Stripe API 2023-08-16 (current)
  └── v2: Stripe API 2025-xx-xx (future, quando necessário)

Config por tenant:
{
  "gateway": "stripe",
  "api_version": "2023-08-16"  // ← tenant pode fixar versão
}
```

Quando um provedor deprecia uma versão de API:
1. Criar novo adapter (`StripeAdapterV2`)
2. Migrar tenants gradualmente (feature flag)
3. Remover adapter antigo após migração completa
4. Sempre backward-compatible dentro da mesma major version

---

## 9. Idempotência

### Regra Universal

Toda operação de integração que **modifica estado externo** DEVE ser idempotente.

```
Mecanismo: Idempotency Key

Sistema gera: idempotency_key = UUID v7
Passa para o adapter.
Adapter envia como header HTTP: Idempotency-Key: <key>

Se o provedor receber a mesma key 2x:
  → Retorna o resultado da primeira chamada (não executa 2x)
```

### Camadas de Idempotência

| Camada | Como |
|--------|------|
| **Aplicação** | Gera idempotency_key antes de chamar adapter |
| **Retry** | Reutiliza a mesma key nas retentativas |
| **DLQ** | Ao reprocessar da DLQ, usa a key original |
| **Webhook** | Gateway envia `idempotency_key` no payload |

---

## 10. Estratégia de Filas (Message Broker)

```
┌──────────────────────────────────────────────────────────────────┐
│                    MESSAGE BROKER (Redis Streams / RabbitMQ)      │
│                                                                   │
│  Stream: integrations.notifications                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Event: notification.send                                     │ │
│  │ {                                                            │ │
│  │   "channel": "whatsapp",                                     │ │
│  │   "tenant_id": "t_001",                                      │ │
│  │   "to": "+5511999999999",                                    │ │
│  │   "template": "booking_confirmation",                        │ │
│  │   "params": { "name": "João", "date": "20/07", ... }        │ │
│  │ }                                                            │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  Consumer Groups:                                                 │
│  ┌────────────────────┐  ┌────────────────────┐                  │
│  │ whatsapp-consumer  │  │ email-consumer     │                  │
│  │ (WhatsAppAdapter)  │  │ (EmailAdapter)     │                  │
│  └────────────────────┘  └────────────────────┘                  │
│  ┌────────────────────┐  ┌────────────────────┐                  │
│  │ sms-consumer       │  │ push-consumer      │                  │
│  │ (SMSAdapter)       │  │ (PushAdapter)      │                  │
│  └────────────────────┘  └────────────────────┘                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 11. Roadmap de Integrações

### MVP (Mês 0-3)
- [x] Nenhuma integração externa (foco no core)
- [x] Infraestrutura de adapters preparada

### V1 (Mês 3-9)
- [ ] **Pagamento:** Stripe (PIX + Cartão)
- [ ] **Notificação:** WhatsApp Cloud API (confirmação + lembrete)
- [ ] **E-mail:** Resend (transactional)
- [ ] **Storage:** Cloudflare R2 (logos, banners)
- [ ] **Google Maps:** Embed no site público

### V2 (Mês 9-18)
- [ ] **Pagamento:** Mercado Pago, PagSeguro (multi-gateway)
- [ ] **SMS:** Twilio/Zenvia (OTP, lembretes)
- [ ] **Google Calendar:** Adicionar evento pós-agendamento
- [ ] **Google Analytics:** Tracking no site público
- [ ] **Meta Pixel:** Conversões de anúncios
- [ ] **Google Login:** OAuth social login

### V3 (Mês 18-36)
- [ ] **Pagamento:** Asaas, Stone (expansão de gateways)
- [ ] **Automação:** Webhooks outbound (n8n, Zapier, Make)
- [ ] **API Pública:** REST API para parceiros
- [ ] **CDN:** Cloudflare Pro (cache, WAF)

### V4 (Mês 36-60)
- [ ] **Marketplace:** Apps de terceiros
- [ ] **OAuth Server:** Login com Barbershop (para apps)
- [ ] **GraphQL API:** Para integrações avançadas

---

> **Resumo:** O Integration Hub é a camada de abstração que isola o sistema principal de qualquer serviço externo. Cada integração é um adapter plugável que implementa uma interface definida pelo domínio. Trocar de provedor é uma mudança de configuração, não de código. Circuit breaker, retry com backoff, DLQ e idempotência garantem resiliência. Logs e métricas garantem observabilidade.
