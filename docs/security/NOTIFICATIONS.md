# 📬 Central de Notificações — Documentação

> **Versão:** 1.0.0 | **Data:** Julho 2026 | **Módulo:** `app.modules.notification`

---

## 1. Visão Geral

Central de Notificações orientada a eventos com **Double Provider Pattern**. Nenhum módulo envia mensagens diretamente — todos publicam eventos no `EventBus`.

### 5 Diferenciais

| # | Diferencial | Descrição |
|---|-------------|-----------|
| **1** | **Event Bus + Double Provider** | Módulos emitem eventos. Central escuta e roteia por canal. Zero acoplamento |
| **2** | **Template Engine** | `{{customer.name}}` resolvido do payload. Versionados. Preview sem enviar |
| **3** | **Smart Delivery Pipeline** | Retry com backoff (1m→5m→15m→1h→6h) + DLQ. Respeita quiet hours |
| **4** | **Idempotency via Event ID** | `UNIQUE(event_id, channel, customer_id)` — mesmo evento não duplica |
| **5** | **Template Preview** | `POST /templates/{id}/preview` renderiza com dados de exemplo |

---

## 2. Arquitetura Event-Driven

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Booking  │  │ Payment  │  │ Customer │  ← Módulos NUNCA enviam diretamente
│ Module   │  │ Module   │  │ Module   │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │              │              │
     │  event_bus.publish(event)   │
     │              │              │
     └──────────────┼──────────────┘
                    │
           ┌────────▼────────┐
           │    EVENT BUS    │  ← Barramento in-process
           └────────┬────────┘
                    │
           ┌────────▼────────┐
           │NotificationSvc  │  ← Escuta eventos
           │ process_event() │
           └────────┬────────┘
                    │
       ┌────────────┼────────────┐
       │            │            │
  ┌────▼────┐ ┌─────▼────┐ ┌────▼────┐
  │WhatsApp │ │  Email   │ │   SMS   │  ← Channel Providers
  │Provider │ │ Provider │ │Provider │
  └─────────┘ └──────────┘ └─────────┘
```

### Como Módulos Emitem Eventos

```python
# Em qualquer módulo (ex: SchedulingService após confirmar booking)
from app.modules.notification.domain.interfaces import event_bus, NotificationEvent

await event_bus.publish(NotificationEvent(
    event_id=f"booking_confirmed_{booking.id}",
    tenant_id=tenant_id,
    category="booking_confirmation",
    payload={
        "customer": {"name": "João", "phone": "5511999999999"},
        "booking": {"date": "20/07/2026", "time": "14:30"},
        "professional": {"name": "Maria"},
        "company": {"name": "Studio 27", "logo_url": "..."},
    },
    customer_id="c_123",
    recipient_phone="5511999999999",
))
```

---

## 3. Template Engine

Templates no banco com `{{variaveis}}`:

```
"Olá {{customer.name}}! Seu horário com {{professional.name}}
foi confirmado para {{booking.date}} às {{booking.time}}.

{{company.name}} — Agende pelo site!"
```

**Preview sem enviar:**
```
POST /notifications/templates/{id}/preview
{"sample_data": {"customer": {"name": "João"}, ...}}
→ "Olá João! Seu horário com Maria foi confirmado..."
```

---

## 4. Delivery Pipeline + Retry

| Tentativa | Delay | Comportamento |
|:---------:|:-----:|---------------|
| 1 | Imediato | Primeiro envio |
| 2 | 1 min | Retry |
| 3 | 5 min | Retry |
| 4 | 15 min | Retry |
| 5 | 1 hora | Retry |
| 6 | 6 horas | Último retry → DLQ |

Após 5 falhas → `status=dead` (DLQ). Pode ser reprocessado manualmente.

---

## 5. Como Adicionar Novo Canal

```python
# 1. Criar provider (1 classe)
class TelegramProvider(NotificationChannelProvider):
    async def send(self, to, subject, body, **kwargs): ...
    async def get_status(self, msg_id): ...

# 2. Registrar (1 linha)
NotificationProviderFactory.register("telegram", TelegramProvider)

# 3. Configurar tenant
POST /notifications/channels/config
{"channel": "telegram", "provider": "telegram_bot", "credentials": "..."}
```

---

## 6. Anti-Spam e Anti-Duplicidade

| Mecanismo | Descrição |
|-----------|-----------|
| `UNIQUE(event_id, channel, customer_id)` | Mesmo evento não gera 2 notificações |
| Quiet hours | Empresa configura horário sem notificações |
| Preferências (planejado) | Cliente opt-in/out por canal |
| Rate limit (planejado) | Máximo de N notificações/cliente/dia |
| Consentimento LGPD | `customer_consents` verificado antes de enviar |
