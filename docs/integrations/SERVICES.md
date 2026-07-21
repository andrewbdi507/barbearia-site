# INTEGRATIONS.md — Guia de Integração com Serviços Externos

O Barbershop SaaS usa **Provider Pattern**. Troque de serviço apenas alterando o `.env`.

## Gateways de Pagamento
- **Mercado Pago:** `MERCADOPAGO_ACCESS_TOKEN`, webhook: `/api/v1/webhooks/mercadopago`
- **Stripe:** `STRIPE_SECRET_KEY`, webhook: `/api/v1/webhooks/stripe`  
- **Asaas:** `ASAAS_API_KEY`, webhook: `/api/v1/webhooks/asaas`

## Notificações
- **WhatsApp:** `WHATSAPP_PROVIDER=meta`, `WHATSAPP_ACCESS_TOKEN`
- **Email:** `EMAIL_PROVIDER=resend|smtp|sendgrid|ses`
- **SMS:** `SMS_PROVIDER=twilio|zenvia`

## Storage
- **Local:** `STORAGE_PROVIDER=local` (dev)
- **S3:** `STORAGE_PROVIDER=s3` + `STORAGE_S3_*`
- **R2:** `STORAGE_PROVIDER=r2` + `STORAGE_R2_*`

## Verificação
```bash
curl http://localhost:8000/api/v1/admin/health/services
```

Consulte `.env.example` para todas as variáveis de ambiente disponíveis.
