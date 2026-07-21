"""Tenant Module — Domain Entities.

Entidades puras (plain Python) — sem dependência de ORM.
Representam as regras de negócio do coração do SaaS.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from app.modules.tenant.domain.enums import (
    BillingCycle,
    DomainType,
    PlanTier,
    SubscriptionStatus,
    TenantStatus,
)
from app.modules.tenant.domain.value_objects import PlanLimits, Subdomain


@dataclass
class Plan:
    """Plano de assinatura — define limites e features disponíveis.

    ARMAZENADO NO BANCO (tabela plans) — NUNCA hardcoded.
    """

    id: str
    name: str
    slug: str
    tier: PlanTier
    description: str = ""
    price_monthly: int = 0  # centavos (BRL)
    price_yearly: int = 0  # centavos (BRL)
    limits: PlanLimits = field(default_factory=PlanLimits)
    features: list[str] = field(default_factory=list)
    is_active: bool = True
    is_public: bool = True  # visível na página de pricing
    sort_order: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def exceeds_limit(self, resource: str, current_count: int) -> bool:
        """Verifica se um recurso excede o limite do plano."""
        limit = getattr(self.limits, resource, None)
        if limit is None:
            return False
        if limit == 0:  # 0 = ilimitado
            return False
        return current_count >= limit

    def has_feature(self, feature: str) -> bool:
        return feature in self.features


@dataclass
class Subscription:
    """Assinatura de um tenant a um plano."""

    id: str
    tenant_id: str
    plan_id: str
    status: SubscriptionStatus = SubscriptionStatus.TRIALING
    billing_cycle: BillingCycle = BillingCycle.MONTHLY
    current_period_start: datetime | None = None
    current_period_end: datetime | None = None
    trial_ends_at: datetime | None = None
    cancel_at_period_end: bool = False
    cancelled_at: datetime | None = None
    payment_method: str | None = None
    gateway_subscription_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_active(self) -> bool:
        return self.status in {
            SubscriptionStatus.TRIALING,
            SubscriptionStatus.ACTIVE,
        }

    @property
    def is_trialing(self) -> bool:
        return self.status == SubscriptionStatus.TRIALING

    @property
    def trial_days_remaining(self) -> int:
        if not self.trial_ends_at:
            return 0
        delta = self.trial_ends_at - datetime.now(timezone.utc)
        return max(0, delta.days)


@dataclass
class Tenant:
    """Aggregate Root — Empresa/Cliente da plataforma SaaS.

    TUDO no sistema pertence a um Tenant.
    """

    id: str
    subdomain: Subdomain
    name: str
    slug: str = ""
    status: TenantStatus = TenantStatus.TRIAL
    plan_id: str | None = None
    owner_id: str | None = None  # FK → User (dono)
    trial_ends_at: datetime | None = None
    suspended_at: datetime | None = None
    suspended_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = None

    # Relacionamentos (carregados sob demanda)
    settings: TenantSettings | None = None
    branding: TenantBranding | None = None
    business_hours: list[BusinessHours] = field(default_factory=list)
    domains: list[Domain] = field(default_factory=list)
    social_media: list[SocialMedia] = field(default_factory=list)

    # ============================================================
    # Regras de Negócio
    # ============================================================

    @property
    def is_active(self) -> bool:
        return self.status == TenantStatus.ACTIVE

    @property
    def is_trial(self) -> bool:
        return self.status == TenantStatus.TRIAL

    @property
    def is_suspended(self) -> bool:
        return self.status == TenantStatus.SUSPENDED

    @property
    def trial_days_remaining(self) -> int:
        if not self.trial_ends_at:
            return 0
        delta = self.trial_ends_at - datetime.now(timezone.utc)
        return max(0, delta.days)

    def can_access(self) -> bool:
        """Verifica se o tenant pode acessar a plataforma."""
        if self.status == TenantStatus.DELETED:
            return False
        if self.status == TenantStatus.CANCELLED:
            return False
        return True

    def activate(self) -> None:
        if self.status not in {TenantStatus.TRIAL, TenantStatus.PAST_DUE, TenantStatus.SUSPENDED}:
            raise ValueError(f"Não pode ativar tenant com status '{self.status}'")
        self.status = TenantStatus.ACTIVE
        self.suspended_at = None
        self.suspended_reason = None
        self.trial_ends_at = None

    def suspend(self, reason: str) -> None:
        if self.status == TenantStatus.DELETED:
            raise ValueError("Não pode suspender tenant deletado.")
        self.status = TenantStatus.SUSPENDED
        self.suspended_at = datetime.now(timezone.utc)
        self.suspended_reason = reason

    def cancel(self) -> None:
        if self.status == TenantStatus.DELETED:
            raise ValueError("Tenant já deletado.")
        self.status = TenantStatus.CANCELLED
        self.cancelled_at = datetime.now(timezone.utc)

    def mark_past_due(self) -> None:
        if self.status not in {TenantStatus.ACTIVE, TenantStatus.TRIAL}:
            return
        self.status = TenantStatus.PAST_DUE

    def start_trial(self, days: int = 14) -> None:
        self.status = TenantStatus.TRIAL
        self.trial_ends_at = datetime.now(timezone.utc) + timedelta(days=days)


@dataclass
class TenantSettings:
    """Configurações operacionais do tenant (1:1)."""

    id: str
    tenant_id: str
    timezone: str = "America/Sao_Paulo"
    language: str = "pt-BR"
    currency: str = "BRL"
    date_format: str = "DD/MM/YYYY"
    time_format: str = "24h"
    booking_interval_minutes: int = 30
    booking_advance_hours: int = 2
    cancellation_policy_hours: int = 2
    max_future_bookings_per_customer: int = 5
    require_payment: bool = False
    deposit_type: str = "none"  # none | fixed | percentage
    deposit_value: int = 0  # centavos ou percentual
    notification_preferences: dict[str, bool] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class TenantBranding:
    """Identidade visual do tenant (1:1)."""

    id: str
    tenant_id: str
    logo_url: str | None = None
    logo_dark_url: str | None = None
    favicon_url: str | None = None
    banner_url: str | None = None
    banner_title: str | None = None
    banner_subtitle: str | None = None
    banner_cta_text: str = "Agende Agora"
    primary_color: str = "#1a1a2e"
    secondary_color: str = "#e94560"
    background_color: str = "#f5f5f5"
    surface_color: str = "#ffffff"
    text_color: str = "#333333"
    text_light_color: str = "#666666"
    heading_font: str = "Inter"
    body_font: str = "Inter"
    base_font_size: str = "16px"
    border_radius: str = "8px"
    layout_template: str = "default"
    custom_css: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class BusinessHours:
    """Horário de funcionamento para um dia da semana."""

    id: str
    tenant_id: str
    day_of_week: int  # 0=Monday (ISO)
    is_closed: bool = False
    open_time: str = "09:00"
    close_time: str = "19:00"
    lunch_start: str | None = None
    lunch_end: str | None = None
    slot_duration_minutes: int = 30
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Domain:
    """Domínio associado ao tenant (subdomínio ou domínio próprio)."""

    id: str
    tenant_id: str
    domain_name: str
    domain_type: DomainType = DomainType.SUBDOMAIN
    is_primary: bool = False
    is_verified: bool = False
    verified_at: datetime | None = None
    ssl_status: str = "pending"
    dns_instructions: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = None


@dataclass
class SocialMedia:
    """Link de rede social do tenant."""

    id: str
    tenant_id: str
    platform: str  # instagram, facebook, etc.
    url: str
    is_visible: bool = True
    sort_order: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class TenantMedia:
    """Arquivo de mídia do tenant."""

    id: str
    tenant_id: str
    uploaded_by: str | None = None  # FK → User
    media_type: str = "gallery"  # logo, banner, gallery, etc.
    filename: str = ""
    original_name: str = ""
    mime_type: str = "image/jpeg"
    size_bytes: int = 0
    url: str = ""
    thumbnail_url: str | None = None
    width: int | None = None
    height: int | None = None
    alt_text: str | None = None
    title: str | None = None
    sort_order: int = 0
    is_visible: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = None


@dataclass
class FeatureFlag:
    """Feature flag para liberação gradual de funcionalidades."""

    id: str
    name: str
    description: str = ""
    enabled_for_all: bool = False
    enabled_tenant_ids: list[str] = field(default_factory=list)
    enabled_percentage: int = 0  # 0-100
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def is_enabled_for(self, tenant_id: str) -> bool:
        if self.enabled_for_all:
            return True
        if tenant_id in self.enabled_tenant_ids:
            return True
        if self.enabled_percentage > 0:
            # Hash determinístico: mesmo tenant sempre retorna mesmo resultado
            import hashlib
            hash_int = int(hashlib.md5(tenant_id.encode()).hexdigest(), 16)
            return (hash_int % 100) < self.enabled_percentage
        return False
