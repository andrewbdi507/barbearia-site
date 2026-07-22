"""Tenant Module — Repository Implementation.

Implementa TODOS os contratos definidos em domain/interfaces.py.
Usa SQLAlchemy async e converte models ↔ entities.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.tenant.domain.entities import (
    BusinessHours,
    Domain,
    FeatureFlag,
    Plan,
    SocialMedia,
    Subscription,
    Tenant,
    TenantBranding,
    TenantMedia,
    TenantSettings,
)
from app.modules.tenant.domain.interfaces import (
    IBusinessHoursRepository,
    IDomainRepository,
    IFeatureFlagRepository,
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
from app.modules.tenant.infrastructure.models.tenant_models import (
    BusinessHoursModel,
    DomainModel,
    FeatureFlagModel,
    PlanModel,
    SocialMediaModel,
    SubscriptionModel,
    TenantBrandingModel,
    TenantMediaModel,
    TenantModel,
    TenantSettingsModel,
)


# ============================================================
# Helpers: Model → Entity
# ============================================================

def _plan_to_entity(m: PlanModel) -> Plan:
    return Plan(
        id=m.id,
        name=m.name,
        slug=m.slug,
        tier=m.tier,
        description=m.description or "",
        price_monthly=m.price_monthly,
        price_yearly=m.price_yearly,
        limits=PlanLimits.from_dict(m.limits or {}),
        features=m.features or [],
        themes=m.themes or [],
        ai_tokens=m.ai_tokens,
        max_concurrent_users=m.max_concurrent_users,
        is_active=m.is_active,
        is_public=m.is_public,
        sort_order=m.sort_order,
        created_at=m.created_at,
    )


def _tenant_to_entity(m: TenantModel) -> Tenant:
    tenant = Tenant(
        id=m.id,
        subdomain=Subdomain(m.subdomain),
        name=m.name,
        slug=m.slug,
        status=m.status,
        plan_id=m.plan_id,
        owner_id=m.owner_id,
        trial_ends_at=m.trial_ends_at,
        suspended_at=m.suspended_at,
        suspended_reason=m.suspended_reason,
        metadata=m.extra_data or {},
        created_at=m.created_at,
        updated_at=m.updated_at,
        deleted_at=m.deleted_at,
    )
    if m.settings:
        tenant.settings = _settings_to_entity(m.settings)
    if m.branding:
        tenant.branding = _branding_to_entity(m.branding)
    # Only access relationships if the model was loaded from DB (has pk populated by query)
    # For newly created models, these will be empty lists
    try:
        tenant.business_hours = [_bh_to_entity(bh) for bh in m.business_hours]
    except Exception:
        tenant.business_hours = []
    try:
        tenant.domains = [_domain_to_entity(d) for d in m.domains]
    except Exception:
        tenant.domains = []
    try:
        tenant.social_media = [_sm_to_entity(sm) for sm in m.social_media]
    except Exception:
        tenant.social_media = []
    return tenant


def _settings_to_entity(m: TenantSettingsModel) -> TenantSettings:
    return TenantSettings(
        id=m.id,
        tenant_id=m.tenant_id,
        timezone=m.timezone,
        language=m.language,
        currency=m.currency,
        date_format=m.date_format,
        time_format=m.time_format,
        booking_interval_minutes=m.booking_interval_minutes,
        booking_advance_hours=m.booking_advance_hours,
        cancellation_policy_hours=m.cancellation_policy_hours,
        max_future_bookings_per_customer=m.max_future_bookings_per_customer,
        require_payment=m.require_payment,
        deposit_type=m.deposit_type,
        deposit_value=m.deposit_value,
        notification_preferences=m.notification_preferences or {},
        metadata=m.extra_data or {},
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


def _branding_to_entity(m: TenantBrandingModel) -> TenantBranding:
    return TenantBranding(
        id=m.id,
        tenant_id=m.tenant_id,
        logo_url=m.logo_url,
        logo_dark_url=m.logo_dark_url,
        favicon_url=m.favicon_url,
        banner_url=m.banner_url,
        banner_title=m.banner_title,
        banner_subtitle=m.banner_subtitle,
        banner_cta_text=m.banner_cta_text,
        primary_color=m.primary_color,
        secondary_color=m.secondary_color,
        background_color=m.background_color,
        surface_color=m.surface_color,
        text_color=m.text_color,
        text_light_color=m.text_light_color,
        heading_font=m.heading_font,
        body_font=m.body_font,
        base_font_size=m.base_font_size,
        border_radius=m.border_radius,
        layout_template=m.layout_template,
        custom_css=m.custom_css,
        metadata=m.extra_data or {},
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


def _bh_to_entity(m: BusinessHoursModel) -> BusinessHours:
    return BusinessHours(
        id=m.id,
        tenant_id=m.tenant_id,
        day_of_week=m.day_of_week,
        is_closed=m.is_closed,
        open_time=m.open_time,
        close_time=m.close_time,
        lunch_start=m.lunch_start,
        lunch_end=m.lunch_end,
        slot_duration_minutes=m.slot_duration_minutes,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


def _domain_to_entity(m: DomainModel) -> Domain:
    return Domain(
        id=m.id,
        tenant_id=m.tenant_id,
        domain_name=m.domain_name,
        domain_type=m.domain_type,
        is_primary=m.is_primary,
        is_verified=m.is_verified,
        verified_at=m.verified_at,
        ssl_status=m.ssl_status,
        dns_instructions=m.dns_instructions or {},
        created_at=m.created_at,
        deleted_at=m.deleted_at,
    )


def _sm_to_entity(m: SocialMediaModel) -> SocialMedia:
    return SocialMedia(
        id=m.id,
        tenant_id=m.tenant_id,
        platform=m.platform,
        url=m.url,
        is_visible=m.is_visible,
        sort_order=m.sort_order,
        created_at=m.created_at,
    )


def _media_to_entity(m: TenantMediaModel) -> TenantMedia:
    return TenantMedia(
        id=m.id,
        tenant_id=m.tenant_id,
        uploaded_by=m.uploaded_by,
        media_type=m.media_type,
        filename=m.filename,
        original_name=m.original_name,
        mime_type=m.mime_type,
        size_bytes=m.size_bytes,
        url=m.url,
        thumbnail_url=m.thumbnail_url,
        width=m.width,
        height=m.height,
        alt_text=m.alt_text,
        title=m.title,
        sort_order=m.sort_order,
        is_visible=m.is_visible,
        metadata=m.extra_data or {},
        created_at=m.created_at,
        deleted_at=m.deleted_at,
    )


def _sub_to_entity(m: SubscriptionModel) -> Subscription:
    return Subscription(
        id=m.id,
        tenant_id=m.tenant_id,
        plan_id=m.plan_id,
        status=m.status,
        billing_cycle=m.billing_cycle,
        current_period_start=m.current_period_start,
        current_period_end=m.current_period_end,
        trial_ends_at=m.trial_ends_at,
        cancel_at_period_end=m.cancel_at_period_end,
        cancelled_at=m.cancelled_at,
        payment_method=m.payment_method,
        gateway_subscription_id=m.gateway_subscription_id,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


# ============================================================
# TenantRepository
# ============================================================

class TenantRepository(ITenantRepository):
    """Implementação SQLAlchemy do ITenantRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, tenant_id: str) -> Tenant | None:
        stmt = (
            select(TenantModel)
            .where(TenantModel.id == tenant_id)
            .where(TenantModel.deleted_at.is_(None))
            .options(
                selectinload(TenantModel.settings),
                selectinload(TenantModel.branding),
                selectinload(TenantModel.business_hours),
                selectinload(TenantModel.domains),
                selectinload(TenantModel.social_media),
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return _tenant_to_entity(model) if model else None

    async def get_by_subdomain(self, subdomain: str) -> Tenant | None:
        stmt = (
            select(TenantModel)
            .where(TenantModel.subdomain == subdomain.lower())
            .where(TenantModel.deleted_at.is_(None))
            .options(
                selectinload(TenantModel.settings),
                selectinload(TenantModel.branding),
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return _tenant_to_entity(model) if model else None

    async def get_by_domain(self, domain_name: str) -> Tenant | None:
        # Procura em subdomain + domains customizados
        stmt = (
            select(TenantModel)
            .join(DomainModel, DomainModel.tenant_id == TenantModel.id, isouter=True)
            .where(
                or_(
                    TenantModel.subdomain == domain_name.lower(),
                    DomainModel.domain_name == domain_name.lower(),
                )
            )
            .where(TenantModel.deleted_at.is_(None))
            .where(
                or_(
                    DomainModel.deleted_at.is_(None),
                    DomainModel.deleted_at.is_(None),  # mantém sintaxe
                )
            )
            .options(
                selectinload(TenantModel.settings),
                selectinload(TenantModel.branding),
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return _tenant_to_entity(model) if model else None

    async def list_all(
        self, *, status: str | None = None, offset: int = 0, limit: int = 50
    ) -> tuple[list[Tenant], int]:
        base = select(TenantModel).where(TenantModel.deleted_at.is_(None))
        count_q = select(func.count()).select_from(TenantModel).where(
            TenantModel.deleted_at.is_(None)
        )

        if status:
            base = base.where(TenantModel.status == status)
            count_q = count_q.where(TenantModel.status == status)

        total = (await self._session.execute(count_q)).scalar() or 0

        stmt = (
            base.order_by(TenantModel.created_at.desc())
            .offset(offset)
            .limit(limit)
            .options(selectinload(TenantModel.settings))
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [_tenant_to_entity(m) for m in models], total

    async def create(self, tenant: Tenant) -> Tenant:
        model = TenantModel(
            id=tenant.id,
            subdomain=tenant.subdomain.value,
            name=tenant.name,
            slug=tenant.slug or tenant.subdomain.value,
            status=tenant.status,
            plan_id=tenant.plan_id,
            owner_id=tenant.owner_id,
            trial_ends_at=tenant.trial_ends_at,
            metadata=tenant.metadata,
        )
        self._session.add(model)
        await self._session.flush()

        # Criar settings e branding defaults
        settings = TenantSettingsModel(
            tenant_id=model.id,
            timezone=tenant.settings.timezone if tenant.settings else "America/Sao_Paulo",
            language=tenant.settings.language if tenant.settings else "pt-BR",
        )
        branding = TenantBrandingModel(
            tenant_id=model.id,
            primary_color=tenant.branding.primary_color if tenant.branding else "#1a1a2e",
            secondary_color=tenant.branding.secondary_color if tenant.branding else "#e94560",
        )
        self._session.add_all([settings, branding])
        await self._session.flush()

        model.settings = settings
        model.branding = branding
        return _tenant_to_entity(model)

    async def update(self, tenant: Tenant) -> Tenant:
        stmt = (
            update(TenantModel)
            .where(TenantModel.id == tenant.id)
            .values(
                name=tenant.name,
                slug=tenant.slug,
                status=tenant.status,
                plan_id=tenant.plan_id,
                metadata=tenant.metadata,
                updated_at=datetime.now(timezone.utc),
            )
        )
        await self._session.execute(stmt)
        await self._session.flush()
        # Recarrega
        return await self.get_by_id(tenant.id)  # type: ignore[return-value]

    async def soft_delete(self, tenant_id: str) -> None:
        stmt = (
            update(TenantModel)
            .where(TenantModel.id == tenant_id)
            .values(deleted_at=datetime.now(timezone.utc), status="deleted")
        )
        await self._session.execute(stmt)

    async def update_status(self, tenant_id: str, status: str, reason: str | None = None) -> None:
        values: dict[str, Any] = {"status": status, "updated_at": datetime.now(timezone.utc)}
        if status == "suspended":
            values["suspended_at"] = datetime.now(timezone.utc)
            values["suspended_reason"] = reason
        elif status == "active":
            values["suspended_at"] = None
            values["suspended_reason"] = None
        stmt = update(TenantModel).where(TenantModel.id == tenant_id).values(**values)
        await self._session.execute(stmt)

    async def subdomain_exists(self, subdomain: str, exclude_id: str | None = None) -> bool:
        stmt = select(func.count()).select_from(TenantModel).where(
            TenantModel.subdomain == subdomain.lower()
        )
        if exclude_id:
            stmt = stmt.where(TenantModel.id != exclude_id)
        result = await self._session.execute(stmt)
        return (result.scalar() or 0) > 0

    async def get_usage_counts(self, tenant_id: str) -> dict[str, int]:
        """Retorna contagem de recursos em uso pelo tenant."""
        # Contagens serão implementadas conforme módulos são adicionados
        return {
            "professionals": 0,
            "customers": 0,
            "bookings_this_month": 0,
            "users": 0,
            "integrations": 0,
            "notifications_this_month": 0,
            "upload_storage_mb": 0,
            "gallery_photos": 0,
        }


# ============================================================
# PlanRepository
# ============================================================

class PlanRepository(IPlanRepository):
    """Implementação SQLAlchemy do IPlanRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, plan_id: str) -> Plan | None:
        result = await self._session.execute(
            select(PlanModel).where(PlanModel.id == plan_id)
        )
        model = result.scalar_one_or_none()
        return _plan_to_entity(model) if model else None

    async def get_by_slug(self, slug: str) -> Plan | None:
        result = await self._session.execute(
            select(PlanModel).where(PlanModel.slug == slug)
        )
        model = result.scalar_one_or_none()
        return _plan_to_entity(model) if model else None

    async def list_active(self) -> list[Plan]:
        result = await self._session.execute(
            select(PlanModel)
            .where(PlanModel.is_active.is_(True))
            .where(PlanModel.is_public.is_(True))
            .order_by(PlanModel.sort_order)
        )
        return [_plan_to_entity(m) for m in result.scalars().all()]

    async def list_all(self) -> list[Plan]:
        result = await self._session.execute(
            select(PlanModel).order_by(PlanModel.sort_order)
        )
        return [_plan_to_entity(m) for m in result.scalars().all()]

    async def create(self, plan: Plan) -> Plan:
        model = PlanModel(
            id=plan.id,
            name=plan.name,
            slug=plan.slug,
            tier=plan.tier,
            description=plan.description,
            price_monthly=plan.price_monthly,
            price_yearly=plan.price_yearly,
            limits=plan.limits.to_dict(),
            features=plan.features,
            themes=plan.themes,
            ai_tokens=plan.ai_tokens,
            max_concurrent_users=plan.max_concurrent_users,
            is_active=plan.is_active,
            is_public=plan.is_public,
            sort_order=plan.sort_order,
        )
        self._session.add(model)
        await self._session.flush()
        return _plan_to_entity(model)

    async def update(self, plan: Plan) -> Plan:
        model = await self._session.get(PlanModel, plan.id)
        if not model:
            raise ValueError(f"Plan {plan.id} not found")
        model.name = plan.name
        model.slug = plan.slug
        model.tier = plan.tier
        model.description = plan.description
        model.price_monthly = plan.price_monthly
        model.price_yearly = plan.price_yearly
        model.limits = plan.limits.to_dict()
        model.features = plan.features
        model.themes = plan.themes
        model.ai_tokens = plan.ai_tokens
        model.max_concurrent_users = plan.max_concurrent_users
        model.is_active = plan.is_active
        model.is_public = plan.is_public
        model.sort_order = plan.sort_order
        await self._session.flush()
        return _plan_to_entity(model)


# ============================================================
# SubscriptionRepository
# ============================================================

class SubscriptionRepository(ISubscriptionRepository):
    """Implementação SQLAlchemy do ISubscriptionRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, subscription_id: str) -> Subscription | None:
        result = await self._session.execute(
            select(SubscriptionModel).where(SubscriptionModel.id == subscription_id)
        )
        model = result.scalar_one_or_none()
        return _sub_to_entity(model) if model else None

    async def get_active_for_tenant(self, tenant_id: str) -> Subscription | None:
        result = await self._session.execute(
            select(SubscriptionModel)
            .where(SubscriptionModel.tenant_id == tenant_id)
            .where(
                SubscriptionModel.status.in_(["trialing", "active", "past_due"])
            )
            .order_by(SubscriptionModel.created_at.desc())
            .limit(1)
        )
        model = result.scalar_one_or_none()
        return _sub_to_entity(model) if model else None

    async def get_history_for_tenant(self, tenant_id: str) -> list[Subscription]:
        result = await self._session.execute(
            select(SubscriptionModel)
            .where(SubscriptionModel.tenant_id == tenant_id)
            .order_by(SubscriptionModel.created_at.desc())
        )
        return [_sub_to_entity(m) for m in result.scalars().all()]

    async def create(self, subscription: Subscription) -> Subscription:
        model = SubscriptionModel(
            id=subscription.id,
            tenant_id=subscription.tenant_id,
            plan_id=subscription.plan_id,
            status=subscription.status,
            billing_cycle=subscription.billing_cycle,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            trial_ends_at=subscription.trial_ends_at,
            cancel_at_period_end=subscription.cancel_at_period_end,
            payment_method=subscription.payment_method,
            gateway_subscription_id=subscription.gateway_subscription_id,
        )
        self._session.add(model)
        await self._session.flush()
        return _sub_to_entity(model)

    async def update(self, subscription: Subscription) -> Subscription:
        model = await self._session.get(SubscriptionModel, subscription.id)
        if not model:
            raise ValueError(f"Subscription {subscription.id} not found")
        model.status = subscription.status
        model.billing_cycle = subscription.billing_cycle
        model.current_period_start = subscription.current_period_start
        model.current_period_end = subscription.current_period_end
        model.cancel_at_period_end = subscription.cancel_at_period_end
        model.cancelled_at = subscription.cancelled_at
        model.payment_method = subscription.payment_method
        model.gateway_subscription_id = subscription.gateway_subscription_id
        model.updated_at = datetime.now(timezone.utc)
        await self._session.flush()
        return _sub_to_entity(model)

    async def update_status(self, subscription_id: str, status: str) -> None:
        stmt = (
            update(SubscriptionModel)
            .where(SubscriptionModel.id == subscription_id)
            .values(status=status, updated_at=datetime.now(timezone.utc))
        )
        await self._session.execute(stmt)


# ============================================================
# Repositories (1:1, 1:N simples)
# ============================================================

class TenantSettingsRepository(ITenantSettingsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_for_tenant(self, tenant_id: str) -> TenantSettings | None:
        result = await self._session.execute(
            select(TenantSettingsModel).where(TenantSettingsModel.tenant_id == tenant_id)
        )
        model = result.scalar_one_or_none()
        return _settings_to_entity(model) if model else None

    async def upsert(self, settings: TenantSettings) -> TenantSettings:
        result = await self._session.execute(
            select(TenantSettingsModel).where(
                TenantSettingsModel.tenant_id == settings.tenant_id
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            for field in (
                "timezone", "language", "currency", "date_format", "time_format",
                "booking_interval_minutes", "booking_advance_hours",
                "cancellation_policy_hours", "max_future_bookings_per_customer",
                "require_payment", "deposit_type", "deposit_value",
                "notification_preferences", "metadata",
            ):
                setattr(existing, field, getattr(settings, field))
            existing.updated_at = datetime.now(timezone.utc)
        else:
            existing = TenantSettingsModel(
                id=settings.id,
                tenant_id=settings.tenant_id,
                timezone=settings.timezone,
                language=settings.language,
                currency=settings.currency,
                date_format=settings.date_format,
                time_format=settings.time_format,
            )
            self._session.add(existing)
        await self._session.flush()
        return _settings_to_entity(existing)


class TenantBrandingRepository(ITenantBrandingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_for_tenant(self, tenant_id: str) -> TenantBranding | None:
        result = await self._session.execute(
            select(TenantBrandingModel).where(
                TenantBrandingModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        return _branding_to_entity(model) if model else None

    async def upsert(self, branding: TenantBranding) -> TenantBranding:
        result = await self._session.execute(
            select(TenantBrandingModel).where(
                TenantBrandingModel.tenant_id == branding.tenant_id
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            for field in (
                "logo_url", "logo_dark_url", "favicon_url", "banner_url",
                "banner_title", "banner_subtitle", "banner_cta_text",
                "primary_color", "secondary_color", "background_color",
                "surface_color", "text_color", "text_light_color",
                "heading_font", "body_font", "base_font_size",
                "border_radius", "layout_template", "custom_css", "metadata",
            ):
                setattr(existing, field, getattr(branding, field))
            existing.updated_at = datetime.now(timezone.utc)
        else:
            existing = TenantBrandingModel(
                id=branding.id,
                tenant_id=branding.tenant_id,
                primary_color=branding.primary_color,
                secondary_color=branding.secondary_color,
            )
            self._session.add(existing)
        await self._session.flush()
        return _branding_to_entity(existing)


class BusinessHoursRepository(IBusinessHoursRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_for_tenant(self, tenant_id: str) -> list[BusinessHours]:
        result = await self._session.execute(
            select(BusinessHoursModel)
            .where(BusinessHoursModel.tenant_id == tenant_id)
            .order_by(BusinessHoursModel.day_of_week)
        )
        return [_bh_to_entity(m) for m in result.scalars().all()]

    async def upsert_batch(
        self, tenant_id: str, hours: list[BusinessHours]
    ) -> list[BusinessHours]:
        # Delete existing, insert new
        await self._session.execute(
            update(BusinessHoursModel)
            .where(BusinessHoursModel.tenant_id == tenant_id)
            .values(is_closed=True)  # soft cleanup — replace strategy
        )
        # Wipe and re-insert
        from sqlalchemy import delete as sa_delete
        await self._session.execute(
            sa_delete(BusinessHoursModel).where(
                BusinessHoursModel.tenant_id == tenant_id
            )
        )
        models = [
            BusinessHoursModel(
                id=bh.id,
                tenant_id=tenant_id,
                day_of_week=bh.day_of_week,
                is_closed=bh.is_closed,
                open_time=bh.open_time,
                close_time=bh.close_time,
                lunch_start=bh.lunch_start,
                lunch_end=bh.lunch_end,
                slot_duration_minutes=bh.slot_duration_minutes,
            )
            for bh in hours
        ]
        self._session.add_all(models)
        await self._session.flush()
        return [_bh_to_entity(m) for m in models]


class DomainRepository(IDomainRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_for_tenant(self, tenant_id: str) -> list[Domain]:
        result = await self._session.execute(
            select(DomainModel)
            .where(DomainModel.tenant_id == tenant_id)
            .where(DomainModel.deleted_at.is_(None))
        )
        return [_domain_to_entity(m) for m in result.scalars().all()]

    async def get_by_name(self, domain_name: str) -> Domain | None:
        result = await self._session.execute(
            select(DomainModel).where(DomainModel.domain_name == domain_name.lower())
        )
        model = result.scalar_one_or_none()
        return _domain_to_entity(model) if model else None

    async def create(self, domain: Domain) -> Domain:
        model = DomainModel(
            id=domain.id,
            tenant_id=domain.tenant_id,
            domain_name=domain.domain_name,
            domain_type=domain.domain_type,
            is_primary=domain.is_primary,
            is_verified=domain.is_verified,
            dns_instructions=domain.dns_instructions,
        )
        self._session.add(model)
        await self._session.flush()
        return _domain_to_entity(model)

    async def delete(self, domain_id: str) -> None:
        stmt = (
            update(DomainModel)
            .where(DomainModel.id == domain_id)
            .values(deleted_at=datetime.now(timezone.utc))
        )
        await self._session.execute(stmt)


class SocialMediaRepository(ISocialMediaRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_for_tenant(self, tenant_id: str) -> list[SocialMedia]:
        result = await self._session.execute(
            select(SocialMediaModel)
            .where(SocialMediaModel.tenant_id == tenant_id)
            .order_by(SocialMediaModel.sort_order)
        )
        return [_sm_to_entity(m) for m in result.scalars().all()]

    async def upsert_batch(
        self, tenant_id: str, links: list[SocialMedia]
    ) -> list[SocialMedia]:
        from sqlalchemy import delete as sa_delete
        await self._session.execute(
            sa_delete(SocialMediaModel).where(
                SocialMediaModel.tenant_id == tenant_id
            )
        )
        models = [
            SocialMediaModel(
                id=sm.id,
                tenant_id=tenant_id,
                platform=sm.platform,
                url=sm.url,
                is_visible=sm.is_visible,
                sort_order=sm.sort_order,
            )
            for sm in links
        ]
        self._session.add_all(models)
        await self._session.flush()
        return [_sm_to_entity(m) for m in models]


class TenantMediaRepository(ITenantMediaRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_for_tenant(
        self, tenant_id: str, media_type: str | None = None
    ) -> list[TenantMedia]:
        stmt = select(TenantMediaModel).where(
            TenantMediaModel.tenant_id == tenant_id,
            TenantMediaModel.deleted_at.is_(None),
        )
        if media_type:
            stmt = stmt.where(TenantMediaModel.media_type == media_type)
        stmt = stmt.order_by(TenantMediaModel.sort_order)
        result = await self._session.execute(stmt)
        return [_media_to_entity(m) for m in result.scalars().all()]

    async def create(self, media: TenantMedia) -> TenantMedia:
        model = TenantMediaModel(
            id=media.id,
            tenant_id=media.tenant_id,
            uploaded_by=media.uploaded_by,
            media_type=media.media_type,
            filename=media.filename,
            original_name=media.original_name,
            mime_type=media.mime_type,
            size_bytes=media.size_bytes,
            url=media.url,
            thumbnail_url=media.thumbnail_url,
            width=media.width,
            height=media.height,
            alt_text=media.alt_text,
            title=media.title,
            sort_order=media.sort_order,
            is_visible=media.is_visible,
            metadata=media.extra_data,
        )
        self._session.add(model)
        await self._session.flush()
        return _media_to_entity(model)

    async def delete(self, media_id: str) -> None:
        stmt = (
            update(TenantMediaModel)
            .where(TenantMediaModel.id == media_id)
            .values(deleted_at=datetime.now(timezone.utc))
        )
        await self._session.execute(stmt)


class FeatureFlagRepository(IFeatureFlagRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_name(self, name: str) -> FeatureFlag | None:
        result = await self._session.execute(
            select(FeatureFlagModel).where(FeatureFlagModel.name == name)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return FeatureFlag(
            id=model.id,
            name=model.name,
            description=model.description or "",
            enabled_for_all=model.enabled_for_all,
            enabled_tenant_ids=model.enabled_tenant_ids or [],
            enabled_percentage=model.enabled_percentage,
            created_at=model.created_at,
        )

    async def is_enabled(self, name: str, tenant_id: str) -> bool:
        flag = await self.get_by_name(name)
        if flag is None:
            return False
        return flag.is_enabled_for(tenant_id)
