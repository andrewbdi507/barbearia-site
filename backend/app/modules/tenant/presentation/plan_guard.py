"""PlanGuard — Middleware de limites de plano SaaS.

Verifica se o tenant tem recursos disponíveis antes de permitir
operações que consumam limites do plano.

Uso:
    @router.post("/staff")
    async def create_staff(
        ...
        _plan: dict = Depends(require_plan_limit("max_staff", "profissionais")),
    ):
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.tenant.presentation.dependencies import get_current_tenant
from app.core.exceptions import PlanLimitExceededError


async def require_plan_limit(
    limit_key: str,
    resource_name: str,
    request: Request,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Verifica se o plano do tenant permite a operação.

    Args:
        limit_key: Chave em plan.limits (ex: "max_staff")
        resource_name: Nome legível (ex: "profissionais")

    Raises:
        PlanLimitExceededError: Se o limite foi atingido
    """
    from sqlalchemy import select
    from app.modules.tenant.infrastructure.models.tenant_models import PlanModel

    plan_id = tenant.get("plan_id")
    if not plan_id:
        return tenant  # Sem plano = sem verificação

    result = await session.execute(
        select(PlanModel.limits).where(PlanModel.id == plan_id)
    )
    limits = result.scalar_one_or_none()

    if limits is None:
        return tenant

    max_allowed = limits.get(limit_key, 0)
    if max_allowed == 0:
        return tenant  # 0 = ilimitado

    # Contar uso atual
    current_count = await _count_resource(session, tenant["id"], limit_key)
    if current_count >= max_allowed:
        raise PlanLimitExceededError(
            message=f"Limite de {resource_name} atingido ({current_count}/{max_allowed}). "
            f"Faça upgrade do plano para adicionar mais.",
        )

    return tenant


async def require_plan_feature(
    feature: str,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Verifica se o plano do tenant inclui determinada feature.

    Args:
        feature: Nome da feature (ex: "whatsapp", "reports")

    Raises:
        PlanLimitExceededError: Se o plano não inclui a feature
    """
    from sqlalchemy import select
    from app.modules.tenant.infrastructure.models.tenant_models import PlanModel

    plan_id = tenant.get("plan_id")
    if not plan_id:
        raise PlanLimitExceededError(message="Plano não encontrado.")

    result = await session.execute(
        select(PlanModel.features).where(PlanModel.id == plan_id)
    )
    features = result.scalar_one_or_none()

    if features is None or feature not in features:
        raise PlanLimitExceededError(
            message=f"Funcionalidade '{feature}' não disponível no seu plano. "
            f"Faça upgrade para acessar."
        )

    return tenant


async def _count_resource(
    session: AsyncSession, tenant_id: str, limit_key: str
) -> int:
    """Conta quantos recursos o tenant está usando."""
    from sqlalchemy import select, func

    counts = {
        "max_staff": ("staff_profiles", "tenant_id"),
        "max_customers": ("customers", "tenant_id"),
        "max_bookings_month": ("bookings", "tenant_id"),
    }

    table_col = counts.get(limit_key)
    if not table_col:
        return 0

    table_name, col = table_col
    result = await session.execute(
        select(func.count()).select_from(
            __import__("sqlalchemy").table(
                table_name,
                __import__("sqlalchemy").column(col),
                __import__("sqlalchemy").column("created_at"),
            )
        ).where(
            getattr(
                __import__("sqlalchemy").table(table_name).c, col
            ) == tenant_id
        )
    )
    return result.scalar() or 0
