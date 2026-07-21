"""Tenant Module — Data Transfer Objects.

Pydantic models para entrada/saída da API.
Validação e serialização de dados do tenant.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


def _new_uuid() -> str:
    return str(uuid4())


# ============================================================
# Plan DTOs
# ============================================================

class PlanLimitsDTO(BaseModel):
    """Limites de recursos configuráveis para um plano."""
    max_professionals: int = Field(default=5, ge=0, description="0 = ilimitado")
    max_customers: int = Field(default=500, ge=0)
    max_bookings_per_month: int = Field(default=200, ge=0)
    max_users: int = Field(default=5, ge=0)
    max_integrations: int = Field(default=0, ge=0)
    max_notifications_per_month: int = Field(default=500, ge=0)
    max_upload_storage_mb: int = Field(default=100, ge=0)
    max_gallery_photos: int = Field(default=10, ge=0)
    custom_domain: bool = False
    custom_branding: bool = False
    reports_advanced: bool = False
    whatsapp_integration: bool = False
    api_access: bool = False
    priority_support: bool = False


class PlanCreateRequest(BaseModel):
    """Request para criar plano."""
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=50, pattern=r"^[a-z0-9-]+$")
    tier: str = Field(default="starter", pattern=r"^(starter|pro|premium|enterprise)$")
    description: str | None = None
    price_monthly: int = Field(default=0, ge=0, description="Centavos (BRL)")
    price_yearly: int = Field(default=0, ge=0)
    limits: PlanLimitsDTO = Field(default_factory=PlanLimitsDTO)
    features: list[str] = Field(default_factory=list)
    is_active: bool = True
    is_public: bool = True
    sort_order: int = 0


class PlanResponse(BaseModel):
    """Response com dados do plano."""
    id: str
    name: str
    slug: str
    tier: str
    description: str | None = None
    price_monthly: int
    price_yearly: int
    limits: dict[str, Any]
    features: list[str]
    is_active: bool
    is_public: bool
    sort_order: int


class PlanListResponse(BaseModel):
    """Lista de planos."""
    plans: list[PlanResponse]


# ============================================================
# Tenant DTOs
# ============================================================

class TenantCreateRequest(BaseModel):
    """Request para criar empresa/tenant."""
    subdomain: str = Field(
        ..., min_length=3, max_length=63,
        pattern=r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$",
        description="Subdomínio único: empresa.barbeariaos.com.br",
    )
    name: str = Field(..., min_length=2, max_length=200, description="Nome da empresa")
    slug: str | None = Field(default=None, description="Auto-gerado do subdomínio")
    owner_email: str | None = Field(default=None, description="Email do dono/admin inicial")
    owner_name: str | None = Field(default=None)
    owner_password: str | None = Field(default=None, min_length=8)
    plan_slug: str = Field(default="starter", description="Slug do plano inicial")
    timezone: str = Field(default="America/Sao_Paulo")
    language: str = Field(default="pt-BR", min_length=2, max_length=10)


class TenantUpdateRequest(BaseModel):
    """Request para atualizar tenant."""
    name: str | None = Field(default=None, min_length=2, max_length=200)
    status: str | None = Field(
        default=None, pattern=r"^(active|suspended|cancelled)$"
    )
    metadata: dict[str, Any] | None = None


class TenantResponse(BaseModel):
    """Response com dados do tenant."""
    id: str
    subdomain: str
    name: str
    slug: str
    status: str
    plan_id: str | None = None
    owner_id: str | None = None
    trial_ends_at: datetime | None = None
    suspended_at: datetime | None = None
    suspended_reason: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | None = None
    settings: "TenantSettingsResponse | None" = None
    branding: "TenantBrandingResponse | None" = None
    business_hours: list["BusinessHoursResponse"] = Field(default_factory=list)
    domains: list["DomainResponse"] = Field(default_factory=list)
    social_media: list["SocialMediaResponse"] = Field(default_factory=list)


class TenantListResponse(BaseModel):
    """Lista paginada de tenants."""
    items: list[TenantResponse]
    total: int
    offset: int
    limit: int


# ============================================================
# Settings DTOs
# ============================================================

class TenantSettingsRequest(BaseModel):
    """Request para atualizar configurações."""
    timezone: str | None = None
    language: str | None = None
    currency: str | None = None
    date_format: str | None = None
    time_format: str | None = None
    booking_interval_minutes: int | None = Field(default=None, ge=5, le=120)
    booking_advance_hours: int | None = Field(default=None, ge=0, le=720)
    cancellation_policy_hours: int | None = Field(default=None, ge=0, le=168)
    max_future_bookings_per_customer: int | None = Field(default=None, ge=1, le=50)
    require_payment: bool | None = None
    deposit_type: str | None = Field(default=None, pattern=r"^(none|fixed|percentage)$")
    deposit_value: int | None = Field(default=None, ge=0)
    notification_preferences: dict[str, bool] | None = None
    metadata: dict[str, Any] | None = None


class TenantSettingsResponse(BaseModel):
    """Response com configurações do tenant."""
    timezone: str
    language: str
    currency: str
    date_format: str
    time_format: str
    booking_interval_minutes: int
    booking_advance_hours: int
    cancellation_policy_hours: int
    max_future_bookings_per_customer: int
    require_payment: bool
    deposit_type: str
    deposit_value: int
    notification_preferences: dict[str, Any]
    metadata: dict[str, Any]


# ============================================================
# Branding DTOs
# ============================================================

class TenantBrandingRequest(BaseModel):
    """Request para atualizar branding."""
    logo_url: str | None = None
    logo_dark_url: str | None = None
    favicon_url: str | None = None
    banner_url: str | None = None
    banner_title: str | None = Field(default=None, max_length=200)
    banner_subtitle: str | None = Field(default=None, max_length=500)
    banner_cta_text: str | None = Field(default=None, max_length=50)
    primary_color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    secondary_color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    background_color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    surface_color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    text_color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    text_light_color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    heading_font: str | None = Field(default=None, max_length=100)
    body_font: str | None = Field(default=None, max_length=100)
    base_font_size: str | None = None
    border_radius: str | None = None
    layout_template: str | None = Field(default=None, max_length=50)
    custom_css: str | None = None
    metadata: dict[str, Any] | None = None


class TenantBrandingResponse(BaseModel):
    """Response com dados de branding."""
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


# ============================================================
# BusinessHours DTOs
# ============================================================

class BusinessHoursRequest(BaseModel):
    """Horário de um dia da semana."""
    day_of_week: int = Field(..., ge=0, le=6)
    is_closed: bool = False
    open_time: str = Field(default="09:00", pattern=r"^\d{2}:\d{2}$")
    close_time: str = Field(default="19:00", pattern=r"^\d{2}:\d{2}$")
    lunch_start: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    lunch_end: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    slot_duration_minutes: int = Field(default=30, ge=5, le=120)


class BusinessHoursResponse(BaseModel):
    """Response com horário do dia."""
    id: str
    day_of_week: int
    is_closed: bool
    open_time: str
    close_time: str
    lunch_start: str | None = None
    lunch_end: str | None = None
    slot_duration_minutes: int


class BusinessHoursBatchRequest(BaseModel):
    """Atualização em lote dos horários da semana."""
    hours: list[BusinessHoursRequest] = Field(..., min_length=7, max_length=7)


# ============================================================
# Domain DTOs
# ============================================================

class DomainCreateRequest(BaseModel):
    """Request para adicionar domínio."""
    domain_name: str = Field(..., min_length=4, max_length=253)
    domain_type: str = Field(default="subdomain", pattern=r"^(subdomain|custom)$")
    is_primary: bool = False


class DomainResponse(BaseModel):
    """Response com dados do domínio."""
    id: str
    domain_name: str
    domain_type: str
    is_primary: bool
    is_verified: bool
    verified_at: datetime | None = None
    ssl_status: str


# ============================================================
# SocialMedia DTOs
# ============================================================

class SocialMediaRequest(BaseModel):
    """Link de rede social."""
    platform: str = Field(..., pattern=r"^(instagram|facebook|tiktok|youtube|twitter|whatsapp|telegram)$")
    url: str = Field(..., max_length=500)
    is_visible: bool = True
    sort_order: int = 0


class SocialMediaResponse(BaseModel):
    """Response com link de rede social."""
    id: str
    platform: str
    url: str
    is_visible: bool
    sort_order: int


class SocialMediaBatchRequest(BaseModel):
    """Atualização em lote das redes sociais."""
    links: list[SocialMediaRequest]


# ============================================================
# Subscription DTOs
# ============================================================

class SubscriptionResponse(BaseModel):
    """Response com dados da assinatura."""
    id: str
    tenant_id: str
    plan_id: str
    status: str
    billing_cycle: str
    current_period_start: datetime | None = None
    current_period_end: datetime | None = None
    trial_ends_at: datetime | None = None
    cancel_at_period_end: bool
    cancelled_at: datetime | None = None
    payment_method: str | None = None


class SubscriptionListResponse(BaseModel):
    """Histórico de assinaturas."""
    subscriptions: list[SubscriptionResponse]


# ============================================================
# Rebuild forward refs
# ============================================================

TenantResponse.model_rebuild()
