# PAYMENTS.md — Fluxo de Pagamento com Sinal

## Visão Geral

O Barbershop SaaS suporta cobrança de **sinal/depósito** para confirmar agendamentos.

### Regra de Negócio

```
Serviço: R$50,00
Depósito: 20% (configurável)
Cliente paga: R$10,00
→ Agendamento CONFIRMED
```

---

## Fluxo Completo

```
1. Cliente escolhe horário
2. Sistema cria booking com status: WAITING_PAYMENT
3. Sistema calcula depósito (20% padrão)
4. Gateway gera cobrança (PIX / Cartão)
5. Cliente paga
6. Gateway envia webhook → POST /api/v1/payments/webhook/{gateway}
7. Sistema valida assinatura
8. Pagamento: PAID
9. Booking: CONFIRMED
10. Horário bloqueado definitivamente

Se pagamento NÃO for feito em 15 minutos:
→ Booking cancelado
→ Horário liberado
```

---

## Gateways Suportados

| Gateway | Métodos | Provider |
|---------|---------|----------|
| **Mercado Pago** | PIX, Cartão, Boleto | `MercadoPagoProvider` |
| **Stripe** | Cartão, Link, Apple Pay | `StripeProvider` |
| **Asaas** | PIX, Boleto, Cartão | `AsaasProvider` |

---

## Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/scheduling/bookings/{id}/pay-deposit` | Inicia pagamento do sinal |
| `POST` | `/api/v1/payments/webhook/mercadopago` | Webhook Mercado Pago |
| `POST` | `/api/v1/payments/webhook/stripe` | Webhook Stripe |
| `POST` | `/api/v1/payments/webhook/asaas` | Webhook Asaas |

---

## Configuração (.env)

```bash
# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=APP_USR-...
MERCADOPAGO_WEBHOOK_SECRET=meu-segredo

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Asaas
ASAAS_API_KEY=$aact_...
ASAAS_WEBHOOK_SECRET=meu-segredo
```

---

## Configuração por Tenant

No endpoint `PUT /api/v1/tenants/me/settings`:

```json
{
  "require_payment": true,
  "deposit_type": "percent",
  "deposit_value": 20
}
```

---

## Segurança

- ✅ NUNCA armazenamos dados de cartão
- ✅ Webhooks validados por HMAC-SHA256
- ✅ Idempotência: mesmo `gateway_event_id` só processa uma vez
- ✅ Anti-replay: timestamp validado no webhook Stripe
- ✅ PCI-DSS: dados de pagamento ficam no gateway
