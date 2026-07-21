# 💳 Billing & Assinaturas

> **Versão:** 1.0.0 | **Data:** Julho 2026

---

## 1. Estrutura de Planos

Planos são **entidades de banco de dados**, NUNCA hardcoded. Para adicionar um novo plano, basta um INSERT:

```sql
INSERT INTO plans (id, name, slug, tier, price_monthly, limits, features)
VALUES (
  'p_gold',
  'Gold',
  'gold',
  'premium',
  29700,  -- R$ 297,00 em centavos
  '{"max_professionals": 15, "max_customers": 2000, ...}',
  '["custom_branding", "whatsapp_integration", "reports_advanced"]'
);
```

### Adicionar Novo Plano Sem Código

1. `INSERT INTO plans` — o plano aparece automaticamente em `GET /plans`
2. `POST /api/v1/plans` — via API de admin
3. Nenhuma alteração de código necessária

---

## 2. Limites por Plano

Cada plano define limites via JSONB. O sistema consulta esses limites em runtime:

```python
# TenantService.validate_limits()
plan = await self._plans.get_by_id(tenant.plan_id)
if plan.exceeds_limit("max_professionals", current_count):
    raise PlanLimitExceededError(...)
```

| Recurso | Campo | 0 = |
|---------|-------|-----|
| Profissionais | `max_professionals` | Ilimitado |
| Clientes | `max_customers` | Ilimitado |
| Agendamentos/mês | `max_bookings_per_month` | Ilimitado |
| Usuários (staff) | `max_users` | Ilimitado |
| Integrações | `max_integrations` | Nenhuma |
| Notificações/mês | `max_notifications_per_month` | Ilimitado |
| Upload storage (MB) | `max_upload_storage_mb` | Ilimitado |
| Fotos na galeria | `max_gallery_photos` | Ilimitado |

---

## 3. Ciclo de Cobrança

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   TRIAL     │────▶│   ACTIVE    │────▶│  PAST_DUE   │
│  14 dias    │     │  Cobrança   │     │  Falha na   │
│  grátis     │     │  recorrente │     │  cobrança   │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                     ┌─────────▼─────────┐
                                     │    SUSPENDED      │
                                     │  3 falhas + sem   │
                                     │  pagamento        │
                                     └───────────────────┘
```

### Estados da Assinatura

| Estado | Significado | Acesso |
|--------|-------------|:------:|
| `trialing` | Período de teste | ✅ |
| `active` | Assinatura paga e ativa | ✅ |
| `past_due` | Cobrança falhou, tentando novamente | ✅ |
| `unpaid` | Não pago | ❌ |
| `cancelled` | Cancelada pelo tenant | ❌ |
| `expired` | Expirada | ❌ |

---

## 4. Upgrade / Downgrade

```python
# PlanService.change_plan()
await plan_service.change_plan(
    tenant_id="t_abc",
    new_plan_slug="pro",
    billing_cycle="monthly",
)
# → Cancela assinatura atual
# → Cria nova assinatura no plano Pro
# → Atualiza tenant com novo plan_id
```

- **Upgrade**: efeito imediato, tenant ganha acesso a novas features
- **Downgrade**: agendado para o fim do período atual (`cancel_at_period_end`)

---

## 5. Gateway de Pagamento (Futuro)

A estrutura está preparada para integração com Stripe/Pagar.me/MercadoPago:

- `gateway_subscription_id` — ID da assinatura no gateway
- `payment_method` — método de pagamento
- Webhooks do gateway atualizam `Subscription.status`

---

## 6. Preparação para Domínio Próprio

A tabela `tenant_domains` já suporta:

```json
{
  "domain_name": "agenda.minhabarbearia.com.br",
  "domain_type": "custom",
  "is_verified": false,
  "dns_instructions": {
    "type": "CNAME",
    "name": "agenda",
    "value": "barbeariaos.com.br",
    "ttl": 3600
  }
}
```

Quando o tenant configurar o DNS e verificarmos, `is_verified = true` e o domínio fica ativo.

**Fluxo futuro:**
1. Tenant adiciona domínio próprio
2. Sistema gera instruções DNS (CNAME ou A record)
3. Tenant configura no provedor DNS dele
4. Sistema verifica (DNS lookup)
5. SSL provisionado automaticamente (Let's Encrypt / Cloudflare)
6. Tenant acessa via `meudominio.com.br`
