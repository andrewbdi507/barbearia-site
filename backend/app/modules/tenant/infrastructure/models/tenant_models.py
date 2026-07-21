"""Tenant Module — SQLAlchemy ORM Models.

9 modelos que implementam o schema multi-tenant.
Todos os modelos de negócio herdam tenant_id do BaseModel.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, BaseModel


# ============================================================
# Plan
# ============================================================

class PlanModel(Base, BaseModel):
    """Plano de assinatura — NUNCA hardcoded, tudo configurável no banco."""

    __tablename__ = "plans"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    tier: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price_monthly: Mapped[int] = mapped_column(Integer, default=0)  # centavos
    price_yearly: Mapped[int] = mapped_column(Integer, default=0)
    limits: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    features: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    tenants: Mapped[list["TenantModel"]] = relationship("TenantModel", back_populates="plan", lazy="selectin", foreign_keys="[TenantModel.plan_id]")
    subscriptions: Mapped[list["SubscriptionModel"]] = relationship("SubscriptionModel", back_populates="plan", lazy="selectin", foreign_keys="[SubscriptionModel.plan_id]"
    )

    def __repr__(self) -> str:
        return f"<Plan {self.slug} ({self.tier})>"


# ============================================================
# Tenant
# ============================================================

class TenantModel(Base, BaseModel):
    """Aggregate Root — Empresa na plataforma SaaS."""

    __tablename__ = "tenants"

    subdomain: Mapped[str] = mapped_column(
        String(63), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="trial", index=True
    )
    plan_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("plans.id", ondelete="SET NULL"), nullable=True, index=True
    )
    owner_id: Mapped[str | None] = mapped_column(
        String(36), nullable=True
    )
    trial_ends_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    suspended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    suspended_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    extra_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )

    # Relationships
    plan: Mapped[PlanModel | None] = relationship("PlanModel", back_populates="tenants", lazy="selectin", foreign_keys=[plan_id])
    settings: Mapped["TenantSettingsModel | None"] = relationship(
        "TenantSettingsModel", back_populates="tenant", uselist=False, lazy="joined"
    )
    branding: Mapped["TenantBrandingModel | None"] = relationship(
        "TenantBrandingModel", back_populates="tenant", uselist=False, lazy="joined"
    )
    business_hours: Mapped[list["BusinessHoursModel"]] = relationship(
        "BusinessHoursModel", back_populates="tenant", lazy="selectin"
    )
    domains: Mapped[list["DomainModel"]] = relationship(
        "DomainModel", back_populates="tenant", lazy="selectin"
    )
    social_media: Mapped[list["SocialMediaModel"]] = relationship(
        "SocialMediaModel", back_populates="tenant", lazy="selectin"
    )
    media: Mapped[list["TenantMediaModel"]] = relationship(
        "TenantMediaModel", back_populates="tenant", lazy="selectin"
    )
    subscriptions: Mapped[list["SubscriptionModel"]] = relationship(
        "SubscriptionModel", back_populates="tenant", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Tenant {self.subdomain} ({self.status})>"


# ============================================================
# Subscription
# ============================================================

class SubscriptionModel(Base, BaseModel):
    """Assinatura de um tenant a um plano."""

    __tablename__ = "subscriptions"

    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    plan_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("plans.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="trialing", index=True
    )
    billing_cycle: Mapped[str] = mapped_column(String(10), nullable=False, default="monthly")
    current_period_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    current_period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    trial_ends_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, default=False)
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gateway_subscription_id: Mapped[str | None] = mapped_column(
        String(200), nullable=True, index=True
    )

    # Relationships
    tenant: Mapped["TenantModel"] = relationship("TenantModel", back_populates="subscriptions", lazy="selectin")
    plan: Mapped["PlanModel"] = relationship("PlanModel", back_populates="subscriptions", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Subscription {self.id} ({self.status})>"


# ============================================================
# TenantSettings (1:1)
# ============================================================

class TenantSettingsModel(Base, BaseModel):
    """Configurações operacionais do tenant — 1:1."""

    __tablename__ = "tenant_settings"

    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, unique=True, index=True,
    )
    timezone: Mapped[str] = mapped_column(String(50), default="America/Sao_Paulo")
    language: Mapped[str] = mapped_column(String(10), default="pt-BR")
    currency: Mapped[str] = mapped_column(String(5), default="BRL")
    date_format: Mapped[str] = mapped_column(String(20), default="DD/MM/YYYY")
    time_format: Mapped[str] = mapped_column(String(10), default="24h")
    booking_interval_minutes: Mapped[int] = mapped_column(Integer, default=30)
    booking_advance_hours: Mapped[int] = mapped_column(Integer, default=2)
    cancellation_policy_hours: Mapped[int] = mapped_column(Integer, default=2)
    max_future_bookings_per_customer: Mapped[int] = mapped_column(Integer, default=5)
    require_payment: Mapped[bool] = mapped_column(Boolean, default=False)
    deposit_type: Mapped[str] = mapped_column(String(20), default="none")
    deposit_value: Mapped[int] = mapped_column(Integer, default=0)
    notification_preferences: Mapped[dict] = mapped_column(JSONB, default=dict)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Relationships
    tenant: Mapped["TenantModel"] = relationship("TenantModel", back_populates="settings", lazy="selectin")


# ============================================================
# TenantBranding (1:1)
# ============================================================

class TenantBrandingModel(Base, BaseModel):
    """Identidade visual e tema do tenant — 1:1."""

    __tablename__ = "tenant_branding"

    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, unique=True, index=True,
    )
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_dark_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    favicon_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    banner_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    banner_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    banner_subtitle: Mapped[str | None] = mapped_column(String(500), nullable=True)
    banner_cta_text: Mapped[str] = mapped_column(String(50), default="Agende Agora")
    primary_color: Mapped[str] = mapped_column(String(7), default="#1a1a2e")
    secondary_color: Mapped[str] = mapped_column(String(7), default="#e94560")
    background_color: Mapped[str] = mapped_column(String(7), default="#f5f5f5")
    surface_color: Mapped[str] = mapped_column(String(7), default="#ffffff")
    text_color: Mapped[str] = mapped_column(String(7), default="#333333")
    text_light_color: Mapped[str] = mapped_column(String(7), default="#666666")
    heading_font: Mapped[str] = mapped_column(String(100), default="Inter")
    body_font: Mapped[str] = mapped_column(String(100), default="Inter")
    base_font_size: Mapped[str] = mapped_column(String(10), default="16px")
    border_radius: Mapped[str] = mapped_column(String(10), default="8px")
    layout_template: Mapped[str] = mapped_column(String(50), default="default")
    custom_css: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Relationships
    tenant: Mapped["TenantModel"] = relationship("TenantModel", back_populates="branding", lazy="selectin")


# ============================================================
# BusinessHours
# ============================================================

class BusinessHoursModel(Base, BaseModel):
    """Horário de funcionamento do tenant por dia da semana."""

    __tablename__ = "business_hours"

    __table_args__ = (
        UniqueConstraint("tenant_id", "day_of_week", name="uq_tenant_day"),
    )

    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    open_time: Mapped[str] = mapped_column(String(5), default="09:00")
    close_time: Mapped[str] = mapped_column(String(5), default="19:00")
    lunch_start: Mapped[str | None] = mapped_column(String(5), nullable=True)
    lunch_end: Mapped[str | None] = mapped_column(String(5), nullable=True)
    slot_duration_minutes: Mapped[int] = mapped_column(Integer, default=30)

    # Relationships
    tenant: Mapped["TenantModel"] = relationship("TenantModel", back_populates="business_hours", lazy="selectin")


# ============================================================
# Domain
# ============================================================

class DomainModel(Base, BaseModel):
    """Domínios do tenant (subdomínio padrão + domínios próprios)."""

    __tablename__ = "tenant_domains"

    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    domain_name: Mapped[str] = mapped_column(
        String(253), unique=True, nullable=False, index=True
    )
    domain_type: Mapped[str] = mapped_column(String(20), default="subdomain")
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    ssl_status: Mapped[str] = mapped_column(String(20), default="pending")
    dns_instructions: Mapped[dict] = mapped_column(JSONB, default=dict)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    tenant: Mapped["TenantModel"] = relationship("TenantModel", back_populates="domains", lazy="selectin")


# ============================================================
# SocialMedia
# ============================================================

class SocialMediaModel(Base, BaseModel):
    """Links de redes sociais do tenant."""

    __tablename__ = "tenant_social_media"

    __table_args__ = (
        UniqueConstraint("tenant_id", "platform", name="uq_tenant_platform"),
    )

    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    platform: Mapped[str] = mapped_column(String(30), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    tenant: Mapped["TenantModel"] = relationship("TenantModel", back_populates="social_media", lazy="selectin")


# ============================================================
# TenantMedia
# ============================================================

class TenantMediaModel(Base, BaseModel):
    """Arquivos de mídia do tenant (galeria, logos, banners)."""

    __tablename__ = "tenant_media"

    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    uploaded_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    media_type: Mapped[str] = mapped_column(
        String(30), nullable=False, default="gallery", index=True
    )
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    original_name: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), default="image/jpeg")
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    alt_text: Mapped[str | None] = mapped_column(String(500), nullable=True)
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    tenant: Mapped["TenantModel"] = relationship("TenantModel", back_populates="media", lazy="selectin")


# ============================================================
# FeatureFlag
# ============================================================

class FeatureFlagModel(Base, BaseModel):
    """Feature flags para liberação gradual."""

    __tablename__ = "feature_flags"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    enabled_for_all: Mapped[bool] = mapped_column(Boolean, default=False)
    enabled_tenant_ids: Mapped[list] = mapped_column(JSONB, default=list)
    enabled_percentage: Mapped[int] = mapped_column(Integer, default=0)
