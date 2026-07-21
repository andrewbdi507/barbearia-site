# 01 — Webhooks

> Padrão único para todos os webhooks (inbound e outbound).  
> Segurança, idempotência, retry, versionamento.

---

## 1. Filosofia

Todo webhook — seja recebido de um gateway de pagamento ou enviado para um cliente — segue exatamente o mesmo padrão. Isso garante previsibilidade, segurança e facilidade de debugging.

---

## 2. Webhook Inbound (Recebidos)

### 2.1 Estrutura do Endpoint

```
POST /api/v1/webhooks/{provider}/{event_type}

Exemplos:
  POST /api/v1/webhooks/stripe/payment_intent
  POST /api/v1/webhooks/mercadopago/payment
  POST /api/v1/webhooks/whatsapp/message_status
```

### 2.2 Fluxo de Processamento

```
┌──────────────────────────────────────────────────────────────────┐
│                    WEBHOOK INBOUND PIPELINE                       │
│                                                                   │
│  1. RECEBER                                                       │
│     POST /api/v1/webhooks/{provider}/{event}                      │
│     Header: X-Webhook-Signature: t=1234567890,v1=abc123...       │
│                                                                   │
│  2. VALIDAR                                                       │
│     ├── IP Allowlist (produção): IP do gateway?                   │
│     ├── Timestamp: |now - header_timestamp| < 5 min?             │
│     ├── Signature: HMAC-SHA256(payload, webhook_secret)?         │
│     └── Schema: payload corresponde ao schema esperado?           │
│                                                                   │
│  3. IDEMPOTÊNCIA                                                  │
│     ├── Extrair idempotency_key do payload                        │
│     ├── Verificar Redis: já processada?                           │
│     ├── Se SIM → Retornar 200 (OK) sem reprocessar               │
│     └── Se NÃO → Continuar                                        │
│                                                                   │
│  4. PROCESSAR                                                     │
│     ├── Roteamento: provider → adapter                            │
│     ├── Adapter.process_webhook(payload)                          │
│     └── Retorna resultado                                         │
│                                                                   │
│  5. REGISTRAR                                                     │
│     ├── Marcar idempotency_key como processada (Redis, TTL 7d)   │
│     ├── Inserir webhook_log no banco (auditoria)                  │
│     └── Métrica: webhook_received_total{provider, event, status} │
│                                                                   │
│  6. RESPONDER                                                     │
│     ├── Sucesso: 200 OK                                           │
│     ├── Falha de validação: 400/401                               │
│     └── Erro interno: 500 (gateway fará retry)                    │
└──────────────────────────────────────────────────────────────────┘
```

### 2.3 Validação de Assinatura

```
Algoritmo: HMAC-SHA256

1. Extrair header: X-Webhook-Signature
   Formato: t={timestamp},v1={signature}

2. Construir signed_payload:
   "{timestamp}.{raw_body}"

3. Calcular expected_signature:
   HMAC-SHA256(webhook_secret, signed_payload)

4. Comparar (constant-time):
   hmac.compare_digest(expected_signature, received_signature)

5. Verificar timestamp:
   abs(now - timestamp) ≤ 300 segundos (5 min)
```

### 2.4 Tabela: webhook_logs

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `provider` | VARCHAR | stripe, mercadopago, whatsapp |
| `event_type` | VARCHAR | payment_intent.succeeded, etc. |
| `idempotency_key` | VARCHAR | Chave de idempotência do gateway |
| `payload_hash` | VARCHAR | SHA-256 do payload (para busca) |
| `headers` | JSONB | Headers recebidos |
| `status` | VARCHAR | received, validated, processed, failed |
| `processing_duration_ms` | INTEGER | Tempo de processamento |
| `error_message` | TEXT | Se falhou |
| `response_status` | INTEGER | HTTP status retornado |
| `created_at` | TIMESTAMPTZ | |

---

## 3. Webhook Outbound (Enviados)

### 3.1 Quando Usar

Webhooks outbound são a **API de eventos** que o Barbershop SaaS expõe para integrações de terceiros (n8n, Zapier, Make) e para a futura API Pública.

### 3.2 Estrutura do Payload

```json
{
  "id": "evt_abc123",
  "type": "booking.created",
  "api_version": "2026-07-20",
  "created_at": "2026-07-20T14:30:00Z",
  "tenant_id": "t_001",
  "data": {
    "booking_id": "b_456",
    "customer_name": "João Silva",
    "professional_name": "Marcos",
    "service": "Corte",
    "date": "2026-07-25",
    "time": "14:30"
  },
  "idempotency_key": "idem_xyz789"
}
```

### 3.3 Headers Enviados

```
Content-Type: application/json
X-Barbershop-Event: booking.created
X-Barbershop-Signature: t=1234567890,v1=abc123def456...
X-Barbershop-Webhook-Id: evt_abc123
X-Barbershop-Idempotency-Key: idem_xyz789
User-Agent: Barbershop-Webhook/1.0
```

### 3.4 Retry Policy (Outbound)

```
┌──────────────────────────────────────────────────────────────────┐
│              WEBHOOK OUTBOUND RETRY                               │
│                                                                   │
│  Tentativa 1: Imediata                                            │
│  Tentativa 2: +1 minuto                                           │
│  Tentativa 3: +5 minutos                                          │
│  Tentativa 4: +15 minutos                                         │
│  Tentativa 5: +1 hora                                             │
│                                                                   │
│  Timeout por tentativa: 10 segundos                               │
│  Sucesso = HTTP 2xx                                                │
│  Após 5 falhas: evento vai para DLQ + notificação ao admin       │
│                                                                   │
│  Endpoint inativo: se 20 falhas consecutivas →                         │
│    Endpoint é marcado como "disabled" e admin é notificado.       │
└──────────────────────────────────────────────────────────────────┘
```

### 3.5 Configuração por Tenant (futuro)

```json
{
  "tenant_id": "t_001",
  "webhook_endpoints": [
    {
      "id": "wh_001",
      "url": "https://meusistema.com/webhooks/barbershop",
      "secret": "whsec_abc123...",
      "events": ["booking.created", "booking.cancelled", "payment.succeeded"],
      "is_active": true,
      "api_version": "2026-07-20"
    }
  ]
}
```

---

## 4. Idempotência em Webhooks

### Princípio

> "Um webhook pode ser entregue mais de uma vez. O receptor DEVE tratá-lo como idempotente."

### Implementação no Receptor (Inbound)

```
Redis Key: webhook:processed:{idempotency_key}
TTL: 7 dias
Valor: timestamp do primeiro processamento

Ao receber:
1. GET webhook:processed:{idempotency_key}
2. Se EXISTS → 200 OK (já processado)
3. Se NOT EXISTS → Processar → SET com TTL 7d
```

### Implementação no Emissor (Outbound)

```
Cada evento enviado carrega:
- X-Barbershop-Idempotency-Key: UUID v7 único
- Mesma key em todas as retentativas do mesmo evento

O receptor DEVE usar essa key para deduplicação.
```

---

## 5. Versionamento de Webhooks

### API Version

Todo webhook carrega a versão no campo `api_version`:

```
Formato: YYYY-MM-DD (data de release da versão)
Exemplo: "2026-07-20"
```

### Política de Versionamento

- **Backward-compatible:** Campos podem ser ADICIONADOS sem mudar versão
- **Breaking changes:** Nova versão de API + período de coexistência (6 meses)
- **Depreciação:** Header `X-API-Deprecation: 2027-01-20` avisa com antecedência
- **Sunset:** Header `Sunset: Sat, 20 Jan 2027 00:00:00 GMT`

---

## 6. Segurança

### Checklist por Webhook

| Check | Inbound | Outbound |
|-------|:-------:|:--------:|
| TLS 1.3 | ✅ | ✅ |
| HMAC Signature | ✅ Verifica | ✅ Assina |
| Timestamp Validation | ✅ ±5 min | ✅ Inclui |
| IP Allowlist | ✅ Produção | ❌ |
| Idempotency Key | ✅ Processa | ✅ Envia |
| Rate Limiting | ✅ 100/min/provider | ✅ Respeita 429 |
| Payload Size Limit | ✅ 1 MB | — |
| Secret Rotation | ✅ 90 dias | ✅ 90 dias |

---

> **Resumo:** Webhooks são o sistema nervoso das integrações. Todo webhook — inbound ou outbound — segue o mesmo padrão de assinatura HMAC, validação de timestamp, idempotência e versionamento. Isso garante que o sistema possa integrar com dezenas de serviços sem reinventar a roda a cada nova integração.
