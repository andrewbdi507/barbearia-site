"""SaaS Metrics — Super Admin Dashboard.

Endpoints para o dono da plataforma SaaS acompanhar:
- MRR (Monthly Recurring Revenue)
- Total de tenants ativos
- Churn rate
- Trial conversion rate
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.infrastructure.database.session import get_async_session
from app.modules.tenant.infrastructure.models.tenant_models import (
    TenantModel, PlanModel, SubscriptionModel,
)

saas_router = APIRouter(prefix="/saas", tags=["SaaS Admin"])


@saas_router.get("/metrics")
async def saas_metrics(
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Métricas da plataforma SaaS (visão super admin)."""
    # Total tenants
    total = await session.scalar(
        select(func.count()).select_from(TenantModel)
    )

    # Active tenants
    active = await session.scalar(
        select(func.count()).select_from(TenantModel).where(TenantModel.status == "active")
    )

    # Trial tenants
    trial = await session.scalar(
        select(func.count()).select_from(TenantModel).where(TenantModel.status == "trial")
    )

    # MRR (Monthly Recurring Revenue)
    mrr_result = await session.execute(
        select(func.sum(PlanModel.price_monthly))
        .select_from(SubscriptionModel)
        .join(PlanModel, SubscriptionModel.plan_id == PlanModel.id)
        .where(SubscriptionModel.status == "active")
    )
    mrr = mrr_result.scalar() or 0

    # Churn (cancelled this month)
    churn = await session.scalar(
        select(func.count()).select_from(TenantModel).where(
            TenantModel.status == "cancelled",
            TenantModel.updated_at >= func.date_trunc("month", func.now()),
        )
    )

    return {
        "total_tenants": total,
        "active_tenants": active,
        "trial_tenants": trial,
        "mrr_cents": mrr,
        "mrr_formatted": f"R$ {(mrr / 100):,.2f}",
        "churn_this_month": churn or 0,
        "conversion_rate": f"{((active / total * 100) if total else 0):.1f}%",
    }


@saas_router.get("/tenants")
async def list_all_tenants(
    session: AsyncSession = Depends(get_async_session),
    limit: int = 20,
    offset: int = 0,
) -> list[dict]:
    """Lista todos os tenants (super admin)."""
    result = await session.execute(
        select(
            TenantModel.id, TenantModel.name, TenantModel.subdomain,
            TenantModel.status, TenantModel.created_at,
        )
        .order_by(TenantModel.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return [
        {"id": r[0], "name": r[1], "subdomain": r[2], "status": r[3], "created_at": str(r[4])}
        for r in result
    ]
