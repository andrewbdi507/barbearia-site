"""Tenant Module — FastAPI Dependencies.

Fornece dependências injetáveis para:
- get_current_tenant: Resolve e valida tenant da requisição
- require_plan_feature: Verifica se plano tem feature específica
- get_tenant_service: Injeta TenantService
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    PlanLimitExceededError,
    SubscriptionRequiredError,
    TenantAccessDeniedError,
    TenantNotFoundError,
)
from app.infrastructure.database.session import get_async_session
from app.modules.tenant.application.tenant_service import TenantService
from app.modules.tenant.infrastructure.cache import TenantRedisCache
from app.modules.tenant.infrastructure.repository import (
    TenantRepository,
    PlanRepository,
    SubscriptionRepository,
    TenantSettingsRepository,
    TenantBrandingRepository,
    BusinessHoursRepository,
    DomainRepository,
    SocialMediaRepository,
)


# ============================================================
# Service Factory
# ============================================================

_tenant_service: TenantService | None = None


def init_tenant_service(redis_client) -> TenantService:
    """Inicializa o TenantService com Redis (chamado no startup)."""
    global _tenant_service
    cache = TenantRedisCache(redis_client)
    # O service é lazy — cria novos repositories por request
    _tenant_service = None  # Será criado por request
    return None  # type: ignore


async def get_tenant_service(
    session: AsyncSession = Depends(get_async_session),
) -> TenantService:
    """Factory que cria TenantService com todos os repositórios.

    NOTA: O cache Redis é injetado via app.state.redis.
    No MVP, retornamos service sem cache Redis (usando cache nulo).
    """
    from app.infrastructure.cache.null_cache import NullTenantCache
    cache = NullTenantCache()

    return TenantService(
        tenant_repo=TenantRepository(session),
        plan_repo=PlanRepository(session),
        sub_repo=SubscriptionRepository(session),
        settings_repo=TenantSettingsRepository(session),
        branding_repo=TenantBrandingRepository(session),
        bh_repo=BusinessHoursRepository(session),
        domain_repo=DomainRepository(session),
        cache=cache,
    )


# ============================================================
# Tenant Dependency
# ============================================================

async def get_current_tenant(
    request: Request,
    service: TenantService = Depends(get_tenant_service),
) -> dict:
    """Resolve e valida o tenant da requisição.

    Extrai tenant_id de (em ordem de prioridade):
    1. request.state.tenant_id (setado por get_current_user)
    2. JWT token no header Authorization
    3. Header X-Tenant-ID
    """
    tenant_id = getattr(request.state, "tenant_id", None)

    # Fallback: extrair do JWT
    if tenant_id is None:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            try:
                from app.modules.auth.infrastructure.security import decode_token
                payload = decode_token(auth[7:])
                tenant_id = payload.get("tenant_id")
            except Exception:
                pass

    # Fallback: header X-Tenant-ID
    if tenant_id is None:
        tenant_id = request.headers.get("X-Tenant-ID")

    if tenant_id is None:
        raise TenantNotFoundError(message="Tenant não identificado na requisição.")

    tenant = await service.check_tenant_access(tenant_id)

    # Inject into request.state for downstream
    request.state.tenant_id = tenant_id

    return {
        "id": tenant.id,
        "subdomain": tenant.subdomain.value,
        "name": tenant.name,
        "status": tenant.status,
        "plan_id": tenant.plan_id,
    }


# ============================================================
# Plan Feature Dependency
# ============================================================

def require_plan_feature(feature: str):
    """Factory: verifica se o plano do tenant tem determinada feature.

    Uso:
        @router.post("/reports/advanced")
        async def advanced_report(
            tenant: Annotated[dict, Depends(require_plan_feature("reports_advanced"))]
        ):
            ...
    """

    async def checker(
        tenant: dict = Depends(get_current_tenant),
        session: AsyncSession = Depends(get_async_session),
    ) -> dict:
        plan_repo = PlanRepository(session)
        plan = await plan_repo.get_by_id(tenant["plan_id"])
        if plan is None or not plan.has_feature(feature):
            raise PlanLimitExceededError(
                message=f"Feature '{feature}' não disponível no seu plano.",
                details={"required_feature": feature},
            )
        return tenant

    return checker
