# 03 — Catálogo de Serviços Terceiros

> Todas as integrações externas catalogadas, com interfaces, contratos e roadmap.

---

## 1. Payment Gateways

### Interface (Domain Port)

```
PaymentGateway (abstract):
  ├── create_payment_intent(amount_cents, currency, metadata) → PaymentIntent
  ├── get_payment_status(gateway_payment_id) → PaymentStatus
  ├── process_webhook(payload, signature) → WebhookResult
  ├── refund(payment_id, amount_cents?, reason?) → RefundResult
  └── cancel_payment(payment_id) → CancelResult
```

### Provedores Catalogados

| Provedor | Métodos | Região | MVP | Status |
|----------|---------|--------|:---:|:------:|
| **Stripe** | PIX, Cartão, Boleto | Global | ❌ | V1 |
| **Mercado Pago** | PIX, Cartão, Boleto | Brasil | ❌ | V2 |
| **PagSeguro** | PIX, Cartão, Boleto | Brasil | ❌ | V2 |
| **Asaas** | PIX, Boleto, Assinatura | Brasil | ❌ | V3 |
| **Stone** | PIX, Cartão (maquininha) | Brasil | ❌ | V3 |

### Configuração por Tenant

```json
{
  "tenant_id": "t_001",
  "gateways": [
    {
      "gateway": "stripe",
      "is_active": true,
      "api_key_encrypted": "aes256...",
      "webhook_secret_encrypted": "aes256...",
      "settings": {
        "pix_enabled": true,
        "credit_card_enabled": true,
        "boleto_enabled": false
      }
    }
  ],
  "default_gateway": "stripe"
}
```

### Dados NUNCA Armazenados

- ✗ Número do cartão (PAN)
- ✗ CVV/CVC
- ✗ Data de validade
- ✗ Nome impresso no cartão
- ✗ Chave PIX do cliente
- ✗ Qualquer dado PCI-DSS escopo

### Dados Armazenados

- ✅ `gateway_payment_id` (ID da transação no gateway)
- ✅ `status` (pending, paid, refunded)
- ✅ `amount` (centavos)
- ✅ `gateway` (qual provedor)
- ✅ `payment_method` (pix, credit_card — sem detalhes)
- ✅ `paid_at`, `refunded_at`

---

## 2. Notification Channels

### Interface (Domain Port)

```
NotificationSender (abstract):
  ├── send(to, template, params, tenant_id) → SendResult
  ├── send_template(to, template_id, params) → SendResult
  └── get_delivery_status(message_id) → DeliveryStatus
```

### Canais Catalogados

| Canal | Provedor | Método | MVP | Status |
|-------|----------|--------|:---:|:------:|
| **WhatsApp** | Meta Cloud API | Template messages | ✅ | MVP |
| **E-mail** | Resend | Transactional API | ❌ | V1 |
| **E-mail** | AWS SES | SMTP / API | ❌ | V2 |
| **SMS** | Twilio | REST API | ❌ | V2 |
| **SMS** | Zenvia | REST API (BR) | ❌ | V2 |
| **Push** | Web Push API | Service Worker | ❌ | V2 |

### Templates de Mensagem

| Evento | Canal | Template |
|--------|-------|----------|
| `booking.created` | WhatsApp | `booking_confirmation` |
| `booking.reminder_24h` | WhatsApp | `booking_reminder_24h` |
| `booking.reminder_1h` | WhatsApp | `booking_reminder_1h` |
| `booking.completed` | WhatsApp | `review_request` |
| `customer.return_30d` | WhatsApp | `return_prompt` |
| `customer.birthday` | WhatsApp | `birthday_offer` |
| Todas | E-mail | Versão HTML do template |
| `auth.otp` | SMS | `otp_code` |

### WhatsApp Cloud API — Fluxo

```
┌──────────────────────────────────────────────────────────────────┐
│              WHATSAPP CLOUD API INTEGRATION                       │
│                                                                   │
│  1. Configuração (por tenant):                                    │
│     - WhatsApp Business Account ID                                │
│     - Phone Number ID                                             │
│     - Access Token (permanent, rotacionado)                       │
│     - Webhook verify token                                        │
│                                                                   │
│  2. Envio de Mensagem:                                            │
│     POST https://graph.facebook.com/v21.0/{phone_id}/messages    │
│     Header: Authorization: Bearer {token}                         │
│     Body: {                                                       │
│       "messaging_product": "whatsapp",                            │
│       "to": "+5511999999999",                                     │
│       "type": "template",                                         │
│       "template": {                                               │
│         "name": "booking_confirmation",                           │
│         "language": { "code": "pt_BR" },                          │
│         "components": [...]                                       │
│       }                                                           │
│     }                                                             │
│                                                                   │
│  3. Rate Limit:                                                   │
│     - 80 mensagens/segundo (Meta Business)                        │
│     - Throttling interno: 50/segundo                              │
│                                                                   │
│  4. Custos (aproximado, Meta 2026):                               │
│     - Marketing: ~$0.05/conversa                                  │
│     - Utilidade: ~$0.02/conversa                                  │
│     - Service: ~$0.01/conversa                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Storage & CDN

### Interface (Domain Port)

```
StorageProvider (abstract):
  ├── upload(file, path, tenant_id) → UploadResult
  ├── get_url(path, expires_in?) → str
  ├── get_signed_url(path, ttl) → str
  ├── delete(path) → bool
  └── process_image(path, transformations) → ProcessResult
```

### Provedores Catalogados

| Provedor | Uso Principal | Status |
|----------|--------------|:------:|
| **Cloudflare R2** | Storage principal (S3-compatible, sem taxa de egress) | V1 |
| **AWS S3** | Storage (fallback / multi-cloud) | V2 |
| **Cloudflare Images** | Processamento de imagem on-the-fly | V1 |

### Pipeline de Upload

```
┌──────────────────────────────────────────────────────────────────┐
│              IMAGE PROCESSING PIPELINE                            │
│                                                                   │
│  1. Upload (cliente → API)                                        │
│     - Validação: tipo MIME, magic bytes, tamanho ≤ 10 MB        │
│     - Sanitização: renomear para UUID, remover metadados EXIF    │
│                                                                   │
│  2. Storage (API → R2)                                            │
│     - Path: /{tenant_id}/{type}/{uuid}.{ext}                     │
│     - Original preservado (para reprocessamento futuro)           │
│                                                                   │
│  3. Processing (Async Worker)                                     │
│     - Gerar: WebP (lossy, quality 85)                            │
│     - Gerar: AVIF (lossy, quality 70) — fallback WebP            │
│     - Gerar thumbnails: 200w, 400w, 800w, 1200w                  │
│     - CDN URL com transformação on-the-fly                       │
│                                                                   │
│  4. CDN Delivery                                                  │
│     - URL: https://cdn.barbersaas.com/{tenant_id}/...            │
│     - Cache: 1 ano (immutable, hash no nome)                     │
│     - Transformação: ?width=400&format=webp                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Google Services

| Serviço | Interface | Uso | Status |
|---------|-----------|-----|:------:|
| **Google Maps** | Embed (iframe) + Geocoding API | Mapa no site público, autocomplete endereço | V1 |
| **Google Calendar** | REST API v3 | "Adicionar ao calendário" pós-agendamento | V2 |
| **Google Login** | OAuth 2.0 | Login social (cliente e admin) | V2 |
| **Google Analytics** | gtag.js | Analytics no site público | V2 |
| **Google Tag Manager** | gtag.js | Gerenciamento de tags | V3 |

### Google Calendar — Fluxo

```
┌──────────────────────────────────────────────────────────────────┐
│              GOOGLE CALENDAR INTEGRATION                          │
│                                                                   │
│  Fluxo OAuth:                                                     │
│  1. Cliente clica "Adicionar ao Google Calendar"                 │
│  2. Redirecionado para OAuth consent screen                       │
│  3. Cliente autoriza acesso ao calendar                           │
│  4. Sistema recebe access_token + refresh_token                  │
│  5. Sistema cria evento via API:                                  │
│     POST /calendar/v3/calendars/primary/events                   │
│     {                                                             │
│       "summary": "Corte — Studio 27",                             │
│       "start": { "dateTime": "2026-07-25T14:30:00-03:00" },     │
│       "end": { "dateTime": "2026-07-25T15:00:00-03:00" },       │
│       "location": "Rua Augusta, 1234",                            │
│       "reminders": { "useDefault": false, "overrides": [         │
│         { "method": "popup", "minutes": 30 }                     │
│       ]}                                                          │
│     }                                                             │
│                                                                   │
│  Rate Limit: 1.000.000 queries/dia (Google Calendar API)         │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Meta Services

| Serviço | Interface | Uso | Status |
|---------|-----------|-----|:------:|
| **Instagram Basic Display** | OAuth | Exibir feed no site público | V2 |
| **Facebook Pixel** | SDK JS | Tracking de conversão de anúncios | V2 |
| **Conversions API** | REST API | Eventos server-side | V3 |
| **WhatsApp Cloud API** | REST API | Mensagens transacionais | V1 |

### Instagram Feed — Site Público

```
┌──────────────────────────────────────────────────────────────────┐
│              INSTAGRAM INTEGRATION                                │
│                                                                   │
│  Configuração por tenant:                                         │
│  {                                                                │
│    "instagram_enabled": true,                                     │
│    "instagram_username": "barbeariastudio27",                     │
│    "instagram_access_token_encrypted": "aes256...",               │
│    "instagram_refresh_token_encrypted": "aes256..."               │
│  }                                                                │
│                                                                   │
│  Exibição no site:                                                │
│  - Grid de últimas 9 fotos (cache 1h)                            │
│  - Link para perfil                                               │
│  - Atualização automática via webhook (futuro)                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. Automation & No-Code

| Plataforma | Integração | Status |
|-----------|-----------|:------:|
| **n8n** | Self-hosted, webhooks outbound | V3 |
| **Zapier** | Webhooks outbound + REST API | V3 |
| **Make** | Webhooks outbound + REST API | V3 |

### Arquitetura de Automação

```
┌──────────────────────────────────────────────────────────────────┐
│              AUTOMATION PLATFORM INTEGRATION                      │
│                                                                   │
│  Barbershop SaaS                                                  │
│      │                                                            │
│      │ Event: booking.created                                     │
│      ▼                                                            │
│  ┌──────────────────┐                                             │
│  │ Webhook Outbound │────► POST https://n8n.meusite.com/webhook  │
│  │ Dispatcher       │                                             │
│  └──────────────────┘                                             │
│                                                                   │
│  O cliente pode configurar no n8n/Zapier:                         │
│  "Quando booking.created → enviar WhatsApp + email + Google Sheet"│
└──────────────────────────────────────────────────────────────────┘
```

---

## 7. Estratégia Multi-Provedor

### Fallback Automático

```
┌──────────────────────────────────────────────────────────────────┐
│              MULTI-PROVIDER FALLBACK                              │
│                                                                   │
│  Config por tenant:                                               │
│  {                                                                │
│    "payment": {                                                   │
│      "primary": "stripe",                                         │
│      "fallback": "mercadopago",                                   │
│      "auto_fallback": true                                        │
│    }                                                              │
│  }                                                                │
│                                                                   │
│  Fluxo:                                                           │
│  1. Tentar primary gateway                                        │
│  2. Se falhar (circuit breaker aberto) → tentar fallback         │
│  3. Se fallback também falhar → erro para o usuário              │
│                                                                   │
│  Nota: Fallback automático só para métodos compatíveis            │
│  (ex: PIX no Stripe + PIX no Mercado Pago).                       │
│  Cartão de crédito: cliente precisa escolher novamente.           │
└──────────────────────────────────────────────────────────────────┘
```

---

## 8. Monitoramento de Terceiros

### Health Check por Provedor

| Provedor | Health Check | Frequência |
|----------|-------------|:----------:|
| Stripe | `GET https://api.stripe.com/v1/balance` | 5 min |
| WhatsApp | `GET https://graph.facebook.com/v21.0/{phone_id}` | 5 min |
| Resend | `GET https://api.resend.com/health` | 5 min |
| R2 | `HEAD https://{bucket}.r2.cloudflarestorage.com/health` | 5 min |
| Google Calendar | `GET https://www.googleapis.com/calendar/v3/users/me/calendarList` | 15 min |

### Dashboard de Status de Integrações

```
┌──────────────────────────────────────────────────────────────────┐
│              INTEGRATION STATUS DASHBOARD                          │
│                                                                   │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐       │
│  │ Stripe   │ WhatsApp │ Resend   │ R2       │ Google   │       │
│  │ 🟢 OK    │ 🟢 OK    │ 🟡 Slow  │ 🟢 OK    │ 🟢 OK    │       │
│  │ 180ms    │ 320ms    │ 1.2s     │ 45ms     │ 210ms    │       │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘       │
│                                                                   │
│  Últimas 24h:                                                     │
│  Stripe:     1.234 chamadas, 99.8% sucesso, P95 245ms            │
│  WhatsApp:   856 chamadas,  98.5% sucesso, P95 1.2s              │
│  Resend:     234 chamadas,  100% sucesso,  P95 890ms             │
│  R2:        45 chamadas,   100% sucesso,  P95 120ms              │
└──────────────────────────────────────────────────────────────────┘
```

---

> **Resumo:** O catálogo de serviços terceiros define as interfaces padrão (ports) que todo adapter deve implementar. Cada provedor é uma implementação concreta que pode ser trocada sem impacto no domínio. A estratégia multi-provedor com fallback automático garante resiliência. Health checks contínuos monitoram a disponibilidade de cada serviço.
