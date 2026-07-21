# 💰 Módulo de Pagamentos — Documentação

> **Versão:** 1.0.0 | **Data:** Julho 2026 | **Módulo:** `app.modules.payment`

---

## 1. Visão Geral

Módulo financeiro com **Provider Pattern** — o sistema NUNCA conhece qual gateway está sendo usado. Trocar de MercadoPago para Stripe exige apenas criar um novo provider + configurar no banco.

**PCI-DSS Compliance:** ZERO dados de cartão armazenados. Apenas `gateway_payment_id`.

### 6 Diferenciais

| # | Diferencial | Descrição |
|---|-------------|-----------|
| **1** | **Provider Pattern Puro** | `PaymentProvider` ABC → `MercadoPagoProvider`, `StripeProvider`, `AsaasProvider` |
| **2** | **Event Sourcing Imutável** | Cada mudança de status gera `PaymentEvent` append-only |
| **3** | **Webhook Signature Verification** | HMAC-SHA256 por provider. Replay attack prevenido |
| **4** | **Double-Layer Idempotency** | `idempotency_key` (app) + `UNIQUE(gateway_event_id)` (DB) |
| **5** | **PCI-DSS Zero Storage** | NUNCA armazena número de cartão, CVV ou dados sensíveis |
| **6** | **Async Processing** | Webhook responde 200 imediatamente, processa em background |

---

## 2. Arquitetura Provider Pattern

```
┌──────────────────────────────────────────────────────┐
│                  PaymentService                       │
│         (NUNCA conhece o gateway)                     │
│                                                       │
│   payment = await PaymentProviderFactory.create(       │
│       gateway="mercado_pago"                           │
│   )                                                    │
│   result = await payment.create_payment(payment_data) │
└──────────────────────┬───────────────────────────────┘
                       │
              ┌────────▼────────┐
              │ PaymentProvider │  ← ABC (interface)
              │ (abstract)      │
              └────────┬────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
  ┌────▼────┐   ┌──────▼──────┐  ┌─────▼─────┐
  │Mercado  │   │   Stripe    │  │   Asaas   │
  │  Pago   │   │  Provider   │  │ Provider  │
  └─────────┘   └─────────────┘  └───────────┘
```

### Para Adicionar um Novo Gateway

```python
# 1. Criar nova classe
class PagSeguroProvider(PaymentProvider):
    async def create_payment(self, payment, **kwargs): ...
    def verify_webhook_signature(self, payload, sig, secret): ...
    # ...

# 2. Registrar no factory
PaymentProviderFactory.register("pagseguro", PagSeguroProvider)

# 3. Configurar no banco
POST /api/v1/payments/gateway/config
{"gateway": "pagseguro", "api_key": "...", "webhook_secret": "..."}
```

**Zero alteração no PaymentService.** O sistema continua funcionando.

---

## 3. Fluxo de Confirmação via Webhook

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Cliente  │     │ Backend  │     │ Gateway  │     │   Banco  │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                 │               │                 │
     │ 1. POST /payments│               │                 │
     │─────────────────▶│               │                 │
     │                 │ 2. Create payment              │
     │                 │──────────────▶│                 │
     │                 │               │                 │
     │ 3. Retorna pix_qr_code        │                 │
     │◀────────────────│               │                 │
     │                 │               │                 │
     │ 4. Cliente paga via PIX no app do banco          │
     │═════════════════════════════════▶                 │
     │                 │               │                 │
     │                 │ 5. Webhook    │                 │
     │                 │◀──────────────│                 │
     │                 │               │                 │
     │                 │ 6. Verify signature            │
     │                 │ 7. Check replay (event_id)    │
     │                 │ 8. Update Payment.status=paid  │
     │                 │──────────────────────────────▶│
     │                 │ 9. Log PaymentEvent            │
     │                 │               │                 │
     │                 │ 10. 200 OK    │                 │
     │                 │──────────────▶│                 │
```

**O frontend NUNCA é confiável.** Toda confirmação vem do webhook do gateway.

---

## 4. Segurança

| Mecanismo | Descrição |
|-----------|-----------|
| **Signature verification** | HMAC-SHA256 por provider. Cada gateway tem seu próprio verificador |
| **Replay attack prevention** | `gateway_event_id` UNIQUE no banco. Mesmo webhook 2x → processado 1x |
| **Idempotency keys** | Cliente envia `idempotency_key`. Se mesmo request 2x → retorna existente |
| **PCI-DSS** | ZERO dados de cartão. `gateway_payment_id` é a única referência |
| **API keys encrypted** | `api_key_encrypted` no banco (AES-256-GCM planejado) |
| **Rate limit** | Webhook endpoint com rate limit por IP do gateway |

---

## 5. Escalabilidade

| Estratégia | Descrição |
|------------|-----------|
| **Async webhooks** | Responde 200 imediatamente, processa em background |
| **Event sourcing** | Histórico imutável — sem UPDATE nos eventos |
| **Índices** | `gateway_payment_id` UNIQUE, `idempotency_key` UNIQUE |
| **Filas** | Webhooks → Redis Queue → Worker → DB (planejado) |
