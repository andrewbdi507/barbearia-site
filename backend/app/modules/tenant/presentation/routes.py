"""Tenant Module — API Routes.

Endpoints REST para gerenciamento de:
- Empresas (tenants)
- Planos
- Assinaturas
- Branding
- Configurações
- Horários
- Domínios
- Redes sociais
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.tenant.application.dto import (
    BusinessHoursBatchRequest,
    BusinessHoursResponse,
    DomainCreateRequest,
    DomainResponse,
    PlanCreateRequest,
    PlanListResponse,
    PlanResponse,
    PlanUpdateRequest,
    PlanUsageResponse,
    CheckLimitResponse,
    SocialMediaBatchRequest,
    SocialMediaResponse,
    SubscriptionListResponse,
    SubscriptionResponse,
    TenantBrandingRequest,
    TenantBrandingResponse,
    TenantCreateRequest,
    TenantListResponse,
    TenantResponse,
    TenantSettingsRequest,
    TenantSettingsResponse,
    TenantUpdateRequest,
)
from app.modules.tenant.application.plan_service import PlanService
from app.modules.tenant.application.tenant_service import TenantService
from app.modules.tenant.infrastructure.cache import TenantRedisCache
from app.modules.tenant.infrastructure.repository import (
    BusinessHoursRepository,
    DomainRepository,
    PlanRepository,
    SocialMediaRepository,
    SubscriptionRepository,
    TenantBrandingRepository,
    TenantRepository,
    TenantSettingsRepository,
)
from app.modules.tenant.presentation.dependencies import get_current_tenant, get_tenant_service


# ============================================================
# Routers
# ============================================================

tenant_router = APIRouter(prefix="/tenants", tags=["Tenants"])
plan_router = APIRouter(prefix="/plans", tags=["Plans"])


# ============================================================
# TENANT ENDPOINTS
# ============================================================

@tenant_router.post("", response_model=TenantResponse, status_code=201)
async def create_tenant(
    body: TenantCreateRequest,
    service: TenantService = Depends(get_tenant_service),
) -> TenantResponse:
    """Cria nova empresa com trial de 14 dias, settings e branding padrão."""
    tenant = await service.create_tenant(
        subdomain=body.subdomain,
        name=body.name,
        plan_slug=body.plan_slug,
        tz=body.timezone,
        language=body.language,
    )
    return _tenant_to_response(tenant)


@tenant_router.get("/me", response_model=TenantResponse)
async def get_my_tenant(
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> TenantResponse:
    """Retorna dados completos do tenant autenticado."""
    t = await service.get_tenant(tenant["id"])
    return _tenant_to_response(t)


@tenant_router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: str,
    service: TenantService = Depends(get_tenant_service),
) -> TenantResponse:
    """Retorna dados de um tenant específico (super_admin)."""
    t = await service.get_tenant(tenant_id)
    return _tenant_to_response(t)


@tenant_router.patch("/me", response_model=TenantResponse)
async def update_tenant(
    body: TenantUpdateRequest,
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> TenantResponse:
    """Atualiza dados do tenant."""
    updates = body.model_dump(exclude_none=True)
    t = await service.update_tenant(tenant["id"], **updates)
    return _tenant_to_response(t)


@tenant_router.post("/{tenant_id}/suspend")
async def suspend_tenant(
    tenant_id: str,
    reason: str = "Suspenso pela plataforma.",
    service: TenantService = Depends(get_tenant_service),
) -> dict:
    """Suspende um tenant (super_admin)."""
    await service.suspend_tenant(tenant_id, reason)
    return {"message": "Tenant suspenso.", "tenant_id": tenant_id}


@tenant_router.post("/{tenant_id}/activate")
async def activate_tenant(
    tenant_id: str,
    service: TenantService = Depends(get_tenant_service),
) -> dict:
    """Reativa um tenant suspenso (super_admin)."""
    await service.activate_tenant(tenant_id)
    return {"message": "Tenant ativado.", "tenant_id": tenant_id}


@tenant_router.delete("/{tenant_id}")
async def delete_tenant(
    tenant_id: str,
    service: TenantService = Depends(get_tenant_service),
) -> dict:
    """Soft-delete de um tenant (super_admin)."""
    await service.delete_tenant(tenant_id)
    return {"message": "Tenant removido."}


# ============================================================
# SETTINGS ENDPOINTS
# ============================================================

@tenant_router.get("/me/settings", response_model=TenantSettingsResponse)
async def get_settings(
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> TenantSettingsResponse:
    s = await service.get_settings(tenant["id"])
    return TenantSettingsResponse(**s.__dict__)


@tenant_router.put("/me/settings", response_model=TenantSettingsResponse)
async def update_settings(
    body: TenantSettingsRequest,
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> TenantSettingsResponse:
    s = await service.update_settings(tenant["id"], **body.model_dump(exclude_none=True))
    return TenantSettingsResponse(**s.__dict__)


# ============================================================
# BRANDING ENDPOINTS
# ============================================================

@tenant_router.get("/me/branding", response_model=TenantBrandingResponse)
async def get_branding(
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> TenantBrandingResponse:
    b = await service.get_branding(tenant["id"])
    return TenantBrandingResponse(**b.__dict__)


@tenant_router.put("/me/branding", response_model=TenantBrandingResponse)
async def update_branding(
    body: TenantBrandingRequest,
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> TenantBrandingResponse:
    b = await service.update_branding(tenant["id"], **body.model_dump(exclude_none=True))
    return TenantBrandingResponse(**b.__dict__)


# ============================================================
# BUSINESS HOURS ENDPOINTS
# ============================================================

@tenant_router.get("/me/business-hours", response_model=list[BusinessHoursResponse])
async def get_business_hours(
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> list[BusinessHoursResponse]:
    hours = await service.get_business_hours(tenant["id"])
    return [BusinessHoursResponse(**h.__dict__) for h in hours]


@tenant_router.put("/me/business-hours", response_model=list[BusinessHoursResponse])
async def update_business_hours(
    body: BusinessHoursBatchRequest,
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> list[BusinessHoursResponse]:
    hours = await service.update_business_hours(
        tenant["id"], [h.model_dump() for h in body.hours]
    )
    return [BusinessHoursResponse(**h.__dict__) for h in hours]


# ============================================================
# DOMAIN ENDPOINTS
# ============================================================

@tenant_router.get("/me/domains", response_model=list[DomainResponse])
async def get_domains(
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> list[DomainResponse]:
    domains = await service.get_domains(tenant["id"])
    return [DomainResponse(**d.__dict__) for d in domains]


@tenant_router.post("/me/domains", response_model=DomainResponse, status_code=201)
async def add_domain(
    body: DomainCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> DomainResponse:
    d = await service.add_domain(tenant["id"], body.domain_name, body.domain_type)
    return DomainResponse(**d.__dict__)


@tenant_router.delete("/me/domains/{domain_id}")
async def remove_domain(
    domain_id: str,
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> dict:
    await service.remove_domain(domain_id)
    return {"message": "Domínio removido."}


# ============================================================
# SOCIAL MEDIA ENDPOINTS
# ============================================================

@tenant_router.get("/me/social-media", response_model=list[SocialMediaResponse])
async def get_social_media(
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> list[SocialMediaResponse]:
    links = await service.get_social_media(tenant["id"])
    return [SocialMediaResponse(**sm.__dict__) for sm in links]


@tenant_router.put("/me/social-media", response_model=list[SocialMediaResponse])
async def update_social_media(
    body: SocialMediaBatchRequest,
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> list[SocialMediaResponse]:
    links = await service.update_social_media(
        tenant["id"], [link.model_dump() for link in body.links]
    )
    return [SocialMediaResponse(**sm.__dict__) for sm in links]


# ============================================================
# SUBSCRIPTION ENDPOINTS
# ============================================================

@tenant_router.get("/me/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> SubscriptionResponse:
    sub = await service.get_active_subscription(tenant["id"])
    if sub is None:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(message="Nenhuma assinatura ativa.")
    return SubscriptionResponse(**sub.__dict__)


@tenant_router.get("/me/subscription/history", response_model=SubscriptionListResponse)
async def get_subscription_history(
    tenant: dict = Depends(get_current_tenant),
    service: TenantService = Depends(get_tenant_service),
) -> SubscriptionListResponse:
    history = await service.get_subscription_history(tenant["id"])
    return SubscriptionListResponse(
        subscriptions=[SubscriptionResponse(**s.__dict__) for s in history]
    )


# ============================================================
# PLAN ENDPOINTS
# ============================================================

@plan_router.get("", response_model=PlanListResponse)
async def list_plans(
    session: AsyncSession = Depends(get_async_session),
) -> PlanListResponse:
    """Lista planos ativos e públicos (página de pricing)."""
    repo = PlanRepository(session)
    plans = await repo.list_active()
    return PlanListResponse(plans=[
        PlanResponse(
            id=p.id, name=p.name, slug=p.slug, tier=p.tier,
            description=p.description, price_monthly=p.price_monthly,
            price_yearly=p.price_yearly, limits=p.limits.to_dict(),
            features=p.features,
            themes=getattr(p, 'themes', []),
            ai_tokens=getattr(p, 'ai_tokens', None),
            max_concurrent_users=getattr(p, 'max_concurrent_users', None),
            is_active=p.is_active, is_public=p.is_public, sort_order=p.sort_order,
        )
        for p in plans
    ])


@plan_router.get("/all", response_model=PlanListResponse)
async def list_all_plans(
    session: AsyncSession = Depends(get_async_session),
) -> PlanListResponse:
    """Lista TODOS os planos (super admin)."""
    repo = PlanRepository(session)
    plans = await repo.list_all()
    return PlanListResponse(plans=[
        PlanResponse(
            id=p.id, name=p.name, slug=p.slug, tier=p.tier,
            description=p.description, price_monthly=p.price_monthly,
            price_yearly=p.price_yearly, limits=p.limits.to_dict(),
            features=p.features,
            themes=getattr(p, 'themes', []),
            ai_tokens=getattr(p, 'ai_tokens', None),
            max_concurrent_users=getattr(p, 'max_concurrent_users', None),
            is_active=p.is_active, is_public=p.is_public, sort_order=p.sort_order,
        )
        for p in plans
    ])


@plan_router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> PlanResponse:
    """Retorna detalhes de um plano específico."""
    repo = PlanRepository(session)
    plan = await repo.get_by_id(plan_id)
    if plan is None:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(message="Plano não encontrado.")
    return PlanResponse(
        id=plan.id, name=plan.name, slug=plan.slug, tier=plan.tier,
        description=plan.description, price_monthly=plan.price_monthly,
        price_yearly=plan.price_yearly, limits=plan.limits.to_dict(),
        features=plan.features,
        themes=getattr(plan, 'themes', []),
        ai_tokens=getattr(plan, 'ai_tokens', None),
        max_concurrent_users=getattr(plan, 'max_concurrent_users', None),
        is_active=plan.is_active, is_public=plan.is_public, sort_order=plan.sort_order,
    )


@plan_router.post("", response_model=PlanResponse, status_code=201)
async def create_plan(
    body: PlanCreateRequest,
    session: AsyncSession = Depends(get_async_session),
) -> PlanResponse:
    """Cria um novo plano (super admin)."""
    from app.modules.tenant.application.plan_service import PlanService
    from app.modules.tenant.infrastructure.cache import TenantRedisCache
    cache = TenantRedisCache(None)  # type: ignore
    service = PlanService(
        plan_repo=PlanRepository(session),
        sub_repo=SubscriptionRepository(session),
        tenant_repo=TenantRepository(session),
        cache=cache,
    )
    plan = await service.create_plan(**body.model_dump(exclude_none=True))
    return PlanResponse(
        id=plan.id, name=plan.name, slug=plan.slug, tier=plan.tier,
        description=plan.description, price_monthly=plan.price_monthly,
        price_yearly=plan.price_yearly, limits=plan.limits.to_dict(),
        features=plan.features,
        themes=getattr(plan, 'themes', []),
        ai_tokens=getattr(plan, 'ai_tokens', None),
        max_concurrent_users=getattr(plan, 'max_concurrent_users', None),
        is_active=plan.is_active, is_public=plan.is_public, sort_order=plan.sort_order,
    )


@plan_router.patch("/{plan_id}", response_model=PlanResponse)
async def update_plan(
    plan_id: str,
    body: PlanUpdateRequest,
    session: AsyncSession = Depends(get_async_session),
) -> PlanResponse:
    """Atualiza um plano existente (super admin)."""
    from app.modules.tenant.application.plan_service import PlanService
    from app.modules.tenant.infrastructure.cache import TenantRedisCache
    cache = TenantRedisCache(None)  # type: ignore
    service = PlanService(
        plan_repo=PlanRepository(session),
        sub_repo=SubscriptionRepository(session),
        tenant_repo=TenantRepository(session),
        cache=cache,
    )
    plan = await service.update_plan(plan_id, **body.model_dump(exclude_none=True))
    return PlanResponse(
        id=plan.id, name=plan.name, slug=plan.slug, tier=plan.tier,
        description=plan.description, price_monthly=plan.price_monthly,
        price_yearly=plan.price_yearly, limits=plan.limits.to_dict(),
        features=plan.features,
        themes=getattr(plan, 'themes', []),
        ai_tokens=getattr(plan, 'ai_tokens', None),
        max_concurrent_users=getattr(plan, 'max_concurrent_users', None),
        is_active=plan.is_active, is_public=plan.is_public, sort_order=plan.sort_order,
    )


@plan_router.get("/{plan_id}/usage", response_model=PlanUsageResponse)
async def get_plan_usage(
    plan_id: str,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> PlanUsageResponse:
    """Retorna uso atual do plano para o mês corrente."""
    from datetime import datetime, timezone
    from sqlalchemy import select
    from app.modules.tenant.infrastructure.models.tenant_models import PlanUsageModel, PlanModel

    now = datetime.now(timezone.utc)
    month = now.strftime("%Y-%m")

    # Buscar ou criar registro de uso
    result = await session.execute(
        select(PlanUsageModel).where(
            PlanUsageModel.tenant_id == tenant["id"],
            PlanUsageModel.month == month,
        )
    )
    usage = result.scalar_one_or_none()

    if usage is None:
        usage = PlanUsageModel(
            tenant_id=tenant["id"],
            month=month,
            bookings_count=0,
            ai_tokens_used=0,
        )
        session.add(usage)
        await session.flush()

    # Buscar limites do plano
    plan_result = await session.execute(
        select(PlanModel.limits, PlanModel.ai_tokens).where(PlanModel.id == plan_id)
    )
    plan_row = plan_result.one_or_none()
    limits = plan_row[0] if plan_row else {}
    ai_token_limit = plan_row[1] if plan_row else None

    return PlanUsageResponse(
        tenant_id=tenant["id"],
        month=month,
        bookings_count=usage.bookings_count,
        ai_tokens_used=usage.ai_tokens_used,
        limits={
            **limits,
            "ai_tokens": ai_token_limit,
        },
    )


@plan_router.get("/{plan_id}/check-limit/{resource}", response_model=CheckLimitResponse)
async def check_plan_limit(
    plan_id: str,
    resource: str,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> CheckLimitResponse:
    """Verifica se um recurso está dentro do limite do plano."""
    from app.modules.tenant.presentation.plan_guard import check_resource_limit

    plan_info = await check_resource_limit(
        session, tenant["id"], plan_id, resource,
    )
    return CheckLimitResponse(**plan_info)


# ============================================================
# Response Helpers
# ============================================================

def _tenant_to_response(t) -> TenantResponse:
    return TenantResponse(
        id=t.id,
        subdomain=t.subdomain.value,
        name=t.name,
        slug=t.slug,
        status=t.status,
        plan_id=t.plan_id,
        owner_id=t.owner_id,
        trial_ends_at=t.trial_ends_at,
        suspended_at=t.suspended_at,
        suspended_reason=t.suspended_reason,
        metadata=t.metadata,
        created_at=t.created_at,
        settings=TenantSettingsResponse(**t.settings.__dict__) if t.settings else None,
        branding=TenantBrandingResponse(**t.branding.__dict__) if t.branding else None,
        business_hours=[BusinessHoursResponse(**h.__dict__) for h in t.business_hours],
        domains=[DomainResponse(**d.__dict__) for d in t.domains],
        social_media=[SocialMediaResponse(**s.__dict__) for s in t.social_media],
    )
