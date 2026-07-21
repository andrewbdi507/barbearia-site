# 📢 Marketing, Promoções & Automações — Documentação

> **Versão:** 1.0.0 | **Data:** Julho 2026 | **Módulo:** `app.modules.marketing`

---

## 1. Visão Geral

Módulo completo de Marketing Automation com Rule Engine, cupons, promoções, campanhas e smart segments.

### 5 Diferenciais

| # | Diferencial | Descrição |
|---|-------------|-----------|
| **1** | **Rule Engine** | Evento → Condição → Ação. Regras JSONB no banco. Extensível sem código |
| **2** | **Smart Segments** | VIP, Lapsed 30d, Birthday, High Ticket, New — calculados em tempo real |
| **3** | **Coupon Validator** | Validador centralizado: expiração, limites, valor mínimo, serviços |
| **4** | **Campaign Orchestrator** | Event-driven. Integrado com NotificationCenter |
| **5** | **Anti-Abuse** | Rate limit por cliente/cupom. Uso único via DB constraint |

---

## 2. Rule Engine — Como Funciona

```
Evento (ex: booking.completed)
    │
    ▼
┌─────────────────────────┐
│ Evaluate Conditions      │
│ • status = "completed"   │
│ • total_spent > 50000    │
│ • visits >= 5            │
└─────────┬───────────────┘
          │ todas true
          ▼
┌─────────────────────────┐
│ Execute Actions          │
│ 1. send_coupon (id=c1)  │
│ 2. wait (7 days)        │
│ 3. send_reminder (tpl=t1)│
│ 4. add_tag "Fidelizado" │
└─────────────────────────┘
```

### Criar Nova Automação (API)

```json
POST /marketing/automations
{
  "name": "Cliente Fidelizado",
  "trigger": "booking.completed",
  "conditions": [
    {"field": "total_spent", "operator": "greater_than", "value": 50000}
  ],
  "actions": [
    {"type": "send_coupon", "coupon_id": "c_vip"},
    {"type": "add_tag", "tag": "Fidelizado"}
  ]
}
```

---

## 3. Cupons

| Tipo | Exemplo | Desconto |
|------|---------|:--------:|
| `fixed` | DESCONTO20 | R$ 20,00 fixo |
| `percentage` | BLACK30 | 30% de desconto |
| `first_purchase` | BEMVINDO | 15% na 1ª compra |

### Validação

```
POST /marketing/coupons/validate
{"code": "DESC10", "amount": 5000, "service_id": "s1"}
→ {"valid": true, "discount": 1000, "final_amount": 4000}
```

---

## 4. Smart Segments

| Segmento | Critério |
|----------|----------|
| **VIP** | `total_spent > R$ 1000` |
| **Lapsed 30d** | `last_visit > 30 dias atrás` |
| **High Ticket** | `avg_ticket > R$ 80` |
| **New** | `created_at < 30 dias` |
| **Birthday** | `birth_date.month == now.month` |

---

## 5. Anti-Duplicidade

| Mecanismo | Descrição |
|-----------|-----------|
| `UNIQUE(tenant_id, code)` | Cupom com mesmo código = erro |
| `current_uses >= max_uses` | Cupom esgotado = inválido |
| `max_per_customer` | Cliente usou N vezes = bloqueado |
| `is_valid` property | Verifica ativo + data + usos |
| Rate limit | Max 3 validações/min por IP |
