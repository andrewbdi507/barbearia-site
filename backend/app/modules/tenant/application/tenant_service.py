"""Tenant Module — Application Services.

Orquestra casos de uso do módulo multi-tenant.
NUNCA acessa banco diretamente — usa repositórios (DIP).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.core.exceptions import (
    BusinessRuleError,
    DomainAlreadyTakenError,
    NotFoundError,
    PlanLimitExceededError,
    SubscriptionRequiredError,
    TenantAccessDeniedError,
    TenantNotFoundError,
    TenantSuspendedError,
)
from app.modules.tenant.domain.entities import (
    BusinessHours,
    Domain,
    Plan,
    SocialMedia,
    Subscription,
    Tenant,
    TenantBranding,
    TenantMedia,
    TenantSettings,
)
from app.modules.tenant.domain.enums import (
    BillingCycle,
    DomainType,
    SubscriptionStatus,
    TenantStatus,
)
from app.modules.tenant.domain.interfaces import (
    IBusinessHoursRepository,
    IDomainRepository,
    IPlanRepository,
    ISocialMediaRepository,
    ISubscriptionRepository,
    ITenantBrandingRepository,
    ITenantCache,
    ITenantMediaRepository,
    ITenantRepository,
    ITenantSettingsRepository,
)
from app.modules.tenant.domain.value_objects import PlanLimits, Subdomain


class TenantService:
    """Serviço de orquestração para Tenant (Aggregate Root).

    Responsável por:
    - Criar empresas (com trial, settings, branding default)
    - Gerenciar ciclo de vida (trial → active → suspended → cancelled)
    - Validar limites do plano
    - Garantir isolamento multi-tenant
    """

    def __init__(
        self,
        tenant_repo: ITenantRepository,
        plan_repo: IPlanRepository,
        sub_repo: ISubscriptionRepository,
        settings_repo: ITenantSettingsRepository,
        branding_repo: ITenantBrandingRepository,
        bh_repo: IBusinessHoursRepository,
        domain_repo: IDomainRepository,
        cache: ITenantCache,
    ) -> None:
        self._tenants = tenant_repo
        self._plans = plan_repo
        self._subscriptions = sub_repo
        self._settings = settings_repo
        self._branding = branding_repo
        self._business_hours = bh_repo
        self._domains = domain_repo
        self._cache = cache

    # ============================================================
    # Create Tenant (com trial)
    # ============================================================

    async def create_tenant(
        self,
        subdomain: str,
        name: str,
        plan_slug: str = "starter",
        owner_id: str | None = None,
        tz: str = "America/Sao_Paulo",
        language: str = "pt-BR",
        trial_days: int = 14,
    ) -> Tenant:
        """Cria nova empresa com trial e configurações padrão."""
        subdomain_vo = Subdomain(subdomain.lower())

        # Verificar unicidade do subdomínio
        if await self._tenants.subdomain_exists(subdomain_vo.value):
            raise DomainAlreadyTakenError(
                details={"subdomain": subdomain_vo.value}
            )

        # Buscar plano
        plan = await self._plans.get_by_slug(plan_slug)
        if plan is None:
            raise NotFoundError(message=f"Plano '{plan_slug}' não encontrado.")

        tenant_id = str(uuid4())
        now = datetime.now(timezone.utc)

        # Criar Tenant
        tenant = Tenant(
            id=tenant_id,
            subdomain=subdomain_vo,
            name=name,
            slug=subdomain_vo.value,
            status=TenantStatus.TRIAL,
            plan_id=plan.id,
            owner_id=owner_id,
            trial_ends_at=now + timedelta(days=trial_days),
            settings=TenantSettings(
                id=str(uuid4()),
                tenant_id=tenant_id,
                timezone=tz,
                language=language,
            ),
            branding=TenantBranding(
                id=str(uuid4()),
                tenant_id=tenant_id,
            ),
        )

        # Persistir tenant + settings + branding (em uma transação)
        created = await self._tenants.create(tenant)

        # Criar assinatura trial
        sub = Subscription(
            id=str(uuid4()),
            tenant_id=tenant_id,
            plan_id=plan.id,
            status=SubscriptionStatus.TRIALING,
            billing_cycle=BillingCycle.MONTHLY,
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
            trial_ends_at=now + timedelta(days=trial_days),
        )
        await self._subscriptions.create(sub)

        # Criar domínio padrão (subdomínio)
        domain = Domain(
            id=str(uuid4()),
            tenant_id=tenant_id,
            domain_name=subdomain_vo.value,
            domain_type=DomainType.SUBDOMAIN,
            is_primary=True,
            is_verified=True,
            verified_at=now,
        )
        await self._domains.create(domain)

        # Criar horários padrão (Seg-Sex 09-19, Sab 09-14, Dom fechado)
        default_hours = self._default_business_hours(tenant_id)
        await self._business_hours.upsert_batch(tenant_id, default_hours)

        # Cache
        await self._cache.set_subdomain_mapping(subdomain_vo.value, tenant_id)
        await self._cache.set_tenant(tenant_id, self._tenant_to_cache(created))

        return created

    # ============================================================
    # Get Tenant
    # ============================================================

    async def get_tenant(self, tenant_id: str) -> Tenant:
        """Busca tenant por ID (com cache)."""
        cached = await self._cache.get_tenant(tenant_id)
        if cached:
            return self._cache_to_tenant(cached)

        tenant = await self._tenants.get_by_id(tenant_id)
        if tenant is None:
            raise TenantNotFoundError()

        await self._cache.set_tenant(tenant_id, self._tenant_to_cache(tenant))
        return tenant

    async def get_tenant_by_subdomain(self, subdomain: str) -> Tenant:
        """Resolve tenant pelo subdomínio (com cache)."""
        # Check cache first
        cached_id = await self._cache.get_by_subdomain(subdomain.lower())
        if cached_id:
            return await self.get_tenant(cached_id)

        tenant = await self._tenants.get_by_subdomain(subdomain.lower())
        if tenant is None:
            raise TenantNotFoundError()

        await self._cache.set_subdomain_mapping(subdomain.lower(), tenant.id)
        await self._cache.set_tenant(tenant.id, self._tenant_to_cache(tenant))
        return tenant

    # ============================================================
    # Update Tenant
    # ============================================================

    async def update_tenant(self, tenant_id: str, **kwargs: object) -> Tenant:
        """Atualiza dados do tenant."""
        tenant = await self.get_tenant(tenant_id)
        for key, value in kwargs.items():
            if hasattr(tenant, key) and value is not None:
                setattr(tenant, key, value)

        updated = await self._tenants.update(tenant)
        await self._cache.invalidate_tenant(tenant_id)
        return updated

    # ============================================================
    # Lifecycle
    # ============================================================

    async def activate_tenant(self, tenant_id: str) -> Tenant:
        tenant = await self.get_tenant(tenant_id)
        tenant.activate()
        await self._tenants.update_status(tenant_id, TenantStatus.ACTIVE)
        await self._cache.invalidate_tenant(tenant_id)
        return tenant

    async def suspend_tenant(self, tenant_id: str, reason: str) -> Tenant:
        tenant = await self.get_tenant(tenant_id)
        tenant.suspend(reason)
        await self._tenants.update_status(tenant_id, TenantStatus.SUSPENDED, reason)
        await self._cache.invalidate_tenant(tenant_id)
        return tenant

    async def cancel_tenant(self, tenant_id: str) -> Tenant:
        tenant = await self.get_tenant(tenant_id)
        tenant.cancel()
        await self._tenants.update_status(tenant_id, TenantStatus.CANCELLED)
        await self._cache.invalidate_tenant(tenant_id)
        return tenant

    async def delete_tenant(self, tenant_id: str) -> None:
        await self._tenants.soft_delete(tenant_id)
        await self._cache.invalidate_tenant(tenant_id)

    # ============================================================
    # Plan & Limits
    # ============================================================

    async def validate_limits(self, tenant_id: str, resource: str, current_count: int) -> None:
        """Valida se tenant está dentro dos limites do plano."""
        tenant = await self.get_tenant(tenant_id)
        if not tenant.plan_id:
            return  # Sem plano = sem limites

        plan = await self._plans.get_by_id(tenant.plan_id)
        if plan is None:
            return

        if plan.exceeds_limit(resource, current_count):
            raise PlanLimitExceededError(
                message=f"Limite '{resource}' do plano '{plan.name}' excedido.",
                details={
                    "resource": resource,
                    "current": current_count,
                    "limit": getattr(plan.limits, resource, "N/A"),
                    "plan": plan.slug,
                },
            )

    async def check_tenant_access(self, tenant_id: str) -> Tenant:
        """Verifica se o tenant pode acessar a plataforma.

        Levanta exceção se tenant estiver suspenso, cancelado, etc.
        Usado pelo middleware de tenant em TODA requisição autenticada.
        """
        tenant = await self.get_tenant(tenant_id)

        if not tenant.can_access():
            if tenant.is_suspended:
                raise TenantSuspendedError(
                    details={"reason": tenant.suspended_reason}
                )
            raise TenantAccessDeniedError()

        # Verificar assinatura
        sub = await self._subscriptions.get_active_for_tenant(tenant_id)
        if sub is None and not tenant.is_trial:
            raise SubscriptionRequiredError()

        return tenant

    # ============================================================
    # Settings
    # ============================================================

    async def get_settings(self, tenant_id: str) -> TenantSettings:
        cached = await self._cache.get_settings(tenant_id)
        if cached:
            return TenantSettings(**cached)

        settings = await self._settings.get_for_tenant(tenant_id)
        if settings is None:
            raise NotFoundError(message="Configurações não encontradas.")

        await self._cache.set_settings(tenant_id, self._settings_to_cache(settings))
        return settings

    async def update_settings(self, tenant_id: str, **kwargs: object) -> TenantSettings:
        existing = await self._settings.get_for_tenant(tenant_id)
        if existing is None:
            existing = TenantSettings(id=str(uuid4()), tenant_id=tenant_id)

        for key, value in kwargs.items():
            if hasattr(existing, key) and value is not None:
                setattr(existing, key, value)

        updated = await self._settings.upsert(existing)
        await self._cache.invalidate_tenant(tenant_id)
        return updated

    # ============================================================
    # Branding
    # ============================================================

    async def get_branding(self, tenant_id: str) -> TenantBranding:
        cached = await self._cache.get_branding(tenant_id)
        if cached:
            return TenantBranding(**cached)

        branding = await self._branding.get_for_tenant(tenant_id)
        if branding is None:
            raise NotFoundError(message="Branding não encontrado.")

        await self._cache.set_branding(tenant_id, self._branding_to_cache(branding))
        return branding

    async def update_branding(self, tenant_id: str, **kwargs: object) -> TenantBranding:
        existing = await self._branding.get_for_tenant(tenant_id)
        if existing is None:
            existing = TenantBranding(id=str(uuid4()), tenant_id=tenant_id)

        for key, value in kwargs.items():
            if hasattr(existing, key) and value is not None:
                setattr(existing, key, value)

        updated = await self._branding.upsert(existing)
        await self._cache.invalidate_tenant(tenant_id)
        return updated

    # ============================================================
    # Business Hours
    # ============================================================

    async def get_business_hours(self, tenant_id: str) -> list[BusinessHours]:
        return await self._business_hours.get_for_tenant(tenant_id)

    async def update_business_hours(
        self, tenant_id: str, hours: list[dict]
    ) -> list[BusinessHours]:
        entities = [
            BusinessHours(
                id=str(uuid4()),
                tenant_id=tenant_id,
                day_of_week=h["day_of_week"],
                is_closed=h.get("is_closed", False),
                open_time=h.get("open_time", "09:00"),
                close_time=h.get("close_time", "19:00"),
                lunch_start=h.get("lunch_start"),
                lunch_end=h.get("lunch_end"),
                slot_duration_minutes=h.get("slot_duration_minutes", 30),
            )
            for h in hours
        ]
        result = await self._business_hours.upsert_batch(tenant_id, entities)
        await self._cache.invalidate_tenant(tenant_id)
        return result

    # ============================================================
    # Domains
    # ============================================================

    async def get_domains(self, tenant_id: str) -> list[Domain]:
        return await self._domains.get_for_tenant(tenant_id)

    async def add_domain(self, tenant_id: str, domain_name: str, domain_type: str = "subdomain") -> Domain:
        existing = await self._domains.get_by_name(domain_name.lower())
        if existing:
            raise DomainAlreadyTakenError(details={"domain": domain_name})

        domain = Domain(
            id=str(uuid4()),
            tenant_id=tenant_id,
            domain_name=domain_name.lower(),
            domain_type=domain_type,
            is_primary=False,
        )
        return await self._domains.create(domain)

    async def remove_domain(self, domain_id: str) -> None:
        await self._domains.delete(domain_id)

    # ============================================================
    # Social Media
    # ============================================================

    async def get_social_media(self, tenant_id: str) -> list[SocialMedia]:
        return await self._social_media_repo.get_for_tenant(tenant_id)

    async def update_social_media(
        self, tenant_id: str, links: list[dict]
    ) -> list[SocialMedia]:
        entities = [
            SocialMedia(
                id=str(uuid4()),
                tenant_id=tenant_id,
                platform=link["platform"],
                url=link["url"],
                is_visible=link.get("is_visible", True),
                sort_order=link.get("sort_order", 0),
            )
            for link in links
        ]
        return await self._social_media_repo.upsert_batch(tenant_id, entities)

    # ============================================================
    # Subscription
    # ============================================================

    async def get_active_subscription(self, tenant_id: str) -> Subscription | None:
        return await self._subscriptions.get_active_for_tenant(tenant_id)

    async def get_subscription_history(self, tenant_id: str) -> list[Subscription]:
        return await self._subscriptions.get_history_for_tenant(tenant_id)

    # ============================================================
    # Helpers
    # ============================================================

    @staticmethod
    def _default_business_hours(tenant_id: str) -> list[BusinessHours]:
        """Horários padrão: Seg-Sex 09-19, Sab 09-14, Dom fechado."""
        defaults = [
            (0, "09:00", "19:00", False),  # Mon
            (1, "09:00", "19:00", False),  # Tue
            (2, "09:00", "19:00", False),  # Wed
            (3, "09:00", "19:00", False),  # Thu
            (4, "09:00", "19:00", False),  # Fri
            (5, "09:00", "14:00", False),  # Sat
            (6, "00:00", "00:00", True),   # Sun
        ]
        return [
            BusinessHours(
                id=str(uuid4()),
                tenant_id=tenant_id,
                day_of_week=dow,
                open_time=ot,
                close_time=ct,
                is_closed=closed,
            )
            for dow, ot, ct, closed in defaults
        ]

    @staticmethod
    def _tenant_to_cache(t: Tenant) -> dict:
        return {
            "id": t.id,
            "subdomain": t.subdomain.value,
            "name": t.name,
            "slug": t.slug,
            "status": t.status,
            "plan_id": t.plan_id,
            "owner_id": t.owner_id,
            "trial_ends_at": t.trial_ends_at.isoformat() if t.trial_ends_at else None,
        }

    @staticmethod
    def _cache_to_tenant(data: dict) -> Tenant:
        return Tenant(
            id=data["id"],
            subdomain=Subdomain(data["subdomain"]),
            name=data["name"],
            slug=data.get("slug", data["subdomain"]),
            status=data.get("status", "active"),
            plan_id=data.get("plan_id"),
            owner_id=data.get("owner_id"),
        )

    @staticmethod
    def _settings_to_cache(s: TenantSettings) -> dict:
        return {
            "id": s.id, "tenant_id": s.tenant_id,
            "timezone": s.timezone, "language": s.language,
            "currency": s.currency,
        }

    @staticmethod
    def _branding_to_cache(b: TenantBranding) -> dict:
        return {
            "id": b.id, "tenant_id": b.tenant_id,
            "logo_url": b.logo_url, "primary_color": b.primary_color,
            "secondary_color": b.secondary_color,
        }
