"""PlanGuard — Middleware de limites de plano SaaS.

Verifica se o tenant tem recursos disponíveis antes de permitir
operacoes que consumam limites do plano.

Uso:
    # Limite simples
    @router.post("/staff")
    async def create_staff(
        _plan: dict = Depends(require_plan_limit("max_staff", "profissionais")),
    ): ...

    # Feature gate
    @router.post("/reports/advanced")
    async def advanced_report(
        _plan: dict = Depends(require_plan_feature("reports_advanced")),
    ): ...

    # Tema
    @router.put("/branding/theme")
    async def set_theme(
        _plan: dict = Depends(require_theme_access("dark_premium")),
    ): ...

    # IA tokens
    @router.post("/ai/chat")
    async def ai_chat(
        _plan: dict = Depends(require_ai_tokens(100)),
    ): ...
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.tenant.presentation.dependencies import get_current_tenant
from app.core.exceptions import PlanLimitExceededError


# ============================================================
# Resource Mappers — tabelas associadas a cada limit_key
# ============================================================

_RESOURCE_COUNTS: dict[str, dict[str, str]] = {
    "max_professionals":        {"table": "staff_profiles", "col": "tenant_id"},
    "max_customers":            {"table": "customers", "col": "tenant_id"},
    "max_bookings_per_month":   {"table": "bookings", "col": "tenant_id"},
    "max_users":                {"table": "users", "col": "tenant_id"},
    "max_gallery_photos":       {"table": "gallery_photos", "col": "tenant_id"},
}


# ============================================================
# Plan Limit Guard
# ============================================================

async def require_plan_limit(
    limit_key: str,
    resource_name: str,
    request: Request,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Verifica se o plano do tenant permite a operacao.

    Args:
        limit_key: Chave em plan.limits (ex: "max_staff")
        resource_name: Nome legivel (ex: "profissionais")

    Raises:
        PlanLimitExceededError: Se o limite foi atingido
    """
    from app.modules.tenant.infrastructure.models.tenant_models import PlanModel

    plan_id = tenant.get("plan_id")
    if not plan_id:
        return tenant  # Sem plano = sem verificacao

    result = await session.execute(
        select(PlanModel.limits).where(PlanModel.id == plan_id)
    )
    limits = result.scalar_one_or_none()

    if limits is None:
        return tenant

    max_allowed = limits.get(limit_key, 0)
    if max_allowed == 0:
        return tenant  # 0 = ilimitado

    current_count = await _count_resource(session, tenant["id"], limit_key)
    if current_count >= max_allowed:
        raise PlanLimitExceededError(
            message=f"Limite de {resource_name} atingido ({current_count}/{max_allowed}). "
            f"Faca upgrade do plano para adicionar mais.",
            details={
                "resource": resource_name,
                "current": current_count,
                "max_allowed": max_allowed,
                "remaining": 0,
            },
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
        PlanLimitExceededError: Se o plano nao inclui a feature
    """
    from app.modules.tenant.infrastructure.models.tenant_models import PlanModel

    plan_id = tenant.get("plan_id")
    if not plan_id:
        raise PlanLimitExceededError(message="Plano nao encontrado.")

    result = await session.execute(
        select(PlanModel.features).where(PlanModel.id == plan_id)
    )
    features = result.scalar_one_or_none()

    if features is None or feature not in features:
        raise PlanLimitExceededError(
            message=f"Funcionalidade '{feature}' nao disponivel no seu plano. "
            f"Faca upgrade para acessar.",
            details={"required_feature": feature},
        )

    return tenant


# ============================================================
# Theme Access Guard
# ============================================================

async def require_theme_access(
    theme_slug: str,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Verifica se o plano permite usar determinado tema.

    Args:
        theme_slug: Slug do tema (ex: "dark_premium", "minimal")

    Raises:
        PlanLimitExceededError: Se o plano nao inclui o tema
    """
    from app.modules.tenant.infrastructure.models.tenant_models import PlanModel

    plan_id = tenant.get("plan_id")
    if not plan_id:
        raise PlanLimitExceededError(message="Plano nao encontrado.")

    result = await session.execute(
        select(PlanModel.themes).where(PlanModel.id == plan_id)
    )
    themes = result.scalar_one_or_none()

    if themes is None or theme_slug not in themes:
        raise PlanLimitExceededError(
            message=f"Tema '{theme_slug}' nao disponivel no seu plano. "
            f"Faca upgrade para acessar este tema.",
            details={"required_theme": theme_slug, "available_themes": themes or []},
        )

    return tenant


async def get_plan_themes(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[str]:
    """Retorna lista de slugs de temas disponiveis no plano."""
    from app.modules.tenant.infrastructure.models.tenant_models import PlanModel

    plan_id = tenant.get("plan_id")
    if not plan_id:
        return ["minimal"]

    result = await session.execute(
        select(PlanModel.themes).where(PlanModel.id == plan_id)
    )
    themes = result.scalar_one_or_none()
    return themes if themes else ["minimal"]


# ============================================================
# AI Token Guard
# ============================================================

async def require_ai_tokens(
    tokens_needed: int = 1,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Verifica se o tenant tem tokens de IA disponiveis neste mes.

    Args:
        tokens_needed: Quantos tokens serao consumidos

    Raises:
        PlanLimitExceededError: Se o limite foi atingido
    """
    from app.modules.tenant.infrastructure.models.tenant_models import (
        PlanModel, PlanUsageModel,
    )

    plan_id = tenant.get("plan_id")
    if not plan_id:
        return tenant

    result = await session.execute(
        select(PlanModel.ai_tokens).where(PlanModel.id == plan_id)
    )
    ai_token_limit = result.scalar_one_or_none()

    if ai_token_limit is None:
        return tenant  # null = ilimitado

    now = datetime.now(timezone.utc)
    month = now.strftime("%Y-%m")

    usage_result = await session.execute(
        select(PlanUsageModel.ai_tokens_used).where(
            PlanUsageModel.tenant_id == tenant["id"],
            PlanUsageModel.month == month,
        )
    )
    used = usage_result.scalar_one_or_none() or 0

    if used + tokens_needed > ai_token_limit:
        raise PlanLimitExceededError(
            message=f"Limite de tokens IA atingido ({used}/{ai_token_limit}). "
            f"Faca upgrade para mais tokens.",
            details={
                "resource": "ai_tokens",
                "current": used,
                "max_allowed": ai_token_limit,
                "remaining": 0,
                "needed": tokens_needed,
            },
        )

    return tenant


async def track_ai_token_usage(
    tokens_used: int,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Incrementa o contador de tokens IA do mes corrente."""
    from app.modules.tenant.infrastructure.models.tenant_models import PlanUsageModel

    now = datetime.now(timezone.utc)
    month = now.strftime("%Y-%m")

    result = await session.execute(
        select(PlanUsageModel).where(
            PlanUsageModel.tenant_id == tenant["id"],
            PlanUsageModel.month == month,
        )
    )
    usage = result.scalar_one_or_none()

    if usage:
        usage.ai_tokens_used = (usage.ai_tokens_used or 0) + tokens_used
    else:
        usage = PlanUsageModel(
            tenant_id=tenant["id"],
            month=month,
            bookings_count=0,
            ai_tokens_used=tokens_used,
        )
        session.add(usage)

    await session.flush()


# ============================================================
# Booking Count Guard
# ============================================================

async def require_booking_slot(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Verifica se o tenant ainda tem agendamentos disponiveis no mes."""
    from app.modules.tenant.infrastructure.models.tenant_models import (
        PlanModel, PlanUsageModel,
    )

    plan_id = tenant.get("plan_id")
    if not plan_id:
        return tenant

    result = await session.execute(
        select(PlanModel.limits).where(PlanModel.id == plan_id)
    )
    limits = result.scalar_one_or_none()

    if limits is None:
        return tenant

    max_bookings = limits.get("max_bookings_per_month", 0)
    if max_bookings == 0:
        return tenant

    now = datetime.now(timezone.utc)
    month = now.strftime("%Y-%m")

    usage_result = await session.execute(
        select(PlanUsageModel.bookings_count).where(
            PlanUsageModel.tenant_id == tenant["id"],
            PlanUsageModel.month == month,
        )
    )
    used = usage_result.scalar_one_or_none() or 0

    if used >= max_bookings:
        raise PlanLimitExceededError(
            message=f"Limite de agendamentos do mes atingido ({used}/{max_bookings}). "
            f"Faca upgrade para mais agendamentos.",
            details={
                "resource": "max_bookings_per_month",
                "current": used,
                "max_allowed": max_bookings,
                "remaining": 0,
            },
        )

    return tenant


async def track_booking_count(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Incrementa o contador de agendamentos do mes corrente."""
    from app.modules.tenant.infrastructure.models.tenant_models import PlanUsageModel

    now = datetime.now(timezone.utc)
    month = now.strftime("%Y-%m")

    result = await session.execute(
        select(PlanUsageModel).where(
            PlanUsageModel.tenant_id == tenant["id"],
            PlanUsageModel.month == month,
        )
    )
    usage = result.scalar_one_or_none()

    if usage:
        usage.bookings_count = (usage.bookings_count or 0) + 1
    else:
        usage = PlanUsageModel(
            tenant_id=tenant["id"],
            month=month,
            bookings_count=1,
            ai_tokens_used=0,
        )
        session.add(usage)

    await session.flush()


# ============================================================
# Utility: check_resource_limit
# ============================================================

async def check_resource_limit(
    session: AsyncSession,
    tenant_id: str,
    plan_id: str,
    resource: str,
) -> dict:
    """Retorna {resource, current, max_allowed, remaining, exceeded}.

    Usado pelo endpoint GET /plans/{id}/check-limit/{resource}.
    """
    from app.modules.tenant.infrastructure.models.tenant_models import (
        PlanModel, PlanUsageModel,
    )

    now = datetime.now(timezone.utc)
    month = now.strftime("%Y-%m")

    if resource == "ai_tokens":
        plan_result = await session.execute(
            select(PlanModel.ai_tokens).where(PlanModel.id == plan_id)
        )
        max_allowed = plan_result.scalar_one_or_none()

        usage_result = await session.execute(
            select(PlanUsageModel.ai_tokens_used).where(
                PlanUsageModel.tenant_id == tenant_id,
                PlanUsageModel.month == month,
            )
        )
        current = usage_result.scalar_one_or_none() or 0

    elif resource == "max_bookings_per_month":
        plan_result = await session.execute(
            select(PlanModel.limits).where(PlanModel.id == plan_id)
        )
        limits = plan_result.scalar_one_or_none() or {}
        max_allowed = limits.get("max_bookings_per_month", 0)

        usage_result = await session.execute(
            select(PlanUsageModel.bookings_count).where(
                PlanUsageModel.tenant_id == tenant_id,
                PlanUsageModel.month == month,
            )
        )
        current = usage_result.scalar_one_or_none() or 0

    else:
        plan_result = await session.execute(
            select(PlanModel.limits).where(PlanModel.id == plan_id)
        )
        limits = plan_result.scalar_one_or_none() or {}
        max_allowed = limits.get(resource, 0)

        current = await _count_resource(session, tenant_id, resource)

    unlimited = max_allowed is None or max_allowed == 0
    return {
        "resource": resource,
        "current": current,
        "max_allowed": 0 if unlimited else max_allowed,
        "remaining": -1 if unlimited else max(0, max_allowed - current),
        "exceeded": False if unlimited else (current >= max_allowed),
    }


# ============================================================
# Internal Helpers
# ============================================================

async def _count_resource(
    session: AsyncSession, tenant_id: str, limit_key: str
) -> int:
    """Conta quantos recursos o tenant esta usando no banco."""
    mapping = _RESOURCE_COUNTS.get(limit_key)

    if mapping is None:
        return 0

    table_name = mapping["table"]
    col_name = mapping["col"]

    result = await session.execute(
        text(f"SELECT COUNT(*) FROM {table_name} WHERE {col_name} = :tid"),
        {"tid": tenant_id},
    )
    return result.scalar() or 0
