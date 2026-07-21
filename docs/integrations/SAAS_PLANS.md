# SAAS_PLANS.md — Planos e Assinaturas

## Planos Disponíveis

| Plano | Preço Mensal | Preço Anual | Profissionais | Clientes | Agendamentos/mês |
|-------|:-----------:|:-----------:|:-------------:|:--------:|:----------------:|
| **Starter** | R$49 | R$490 | 1 | 100 | 300 |
| **Professional** | R$99 | R$990 | 5 | Ilimitado | Ilimitado |
| **Premium** | R$199 | R$1.990 | Ilimitado | Ilimitado | Ilimitado |
| **Enterprise** | R$499 | R$4.990 | Ilimitado | Ilimitado | Ilimitado |

## Features por Plano

| Feature | Starter | Professional | Premium | Enterprise |
|---------|:------:|:------------:|:-------:|:----------:|
| Agendamento | ✅ | ✅ | ✅ | ✅ |
| Clientes | ✅ | ✅ | ✅ | ✅ |
| Serviços | ✅ | ✅ | ✅ | ✅ |
| Multi-profissional | ❌ | ✅ (5) | ✅ | ✅ |
| WhatsApp | ❌ | ✅ | ✅ | ✅ |
| Relatórios | ❌ | ✅ | ✅ | ✅ |
| Analytics | ❌ | ❌ | ✅ | ✅ |
| Prioridade | ❌ | ❌ | ✅ | ✅ |
| Automações | ❌ | ❌ | ✅ | ✅ |
| API Pública | ❌ | ❌ | ❌ | ✅ |

## Trial

- **14 dias grátis** para todos os planos
- Sem cartão de crédito necessário
- Após expirar: modo limitado (somente consulta)
- Upgrade a qualquer momento

## PlanGuard

O middleware `require_plan_limit` bloqueia operações que excedem limites:

```python
@router.post("/staff")
async def create_staff(
    ...
    _plan = Depends(require_plan_limit("max_staff", "profissionais")),
):
```

## Métricas SaaS (Super Admin)

`GET /api/v1/saas/metrics`:
```json
{
  "total_tenants": 1,
  "active_tenants": 0,
  "trial_tenants": 1,
  "mrr_cents": 0,
  "mrr_formatted": "R$ 0.00",
  "churn_this_month": 0,
  "conversion_rate": "0.0%"
}
```
