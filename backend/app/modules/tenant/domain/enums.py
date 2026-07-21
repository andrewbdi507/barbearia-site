"""Tenant Module — Domain Enums.

Define TODOS os estados e tipos do módulo multi-tenant.
"""

from __future__ import annotations

from enum import StrEnum


class TenantStatus(StrEnum):
    """Ciclo de vida do tenant.

    trial → active → (past_due → suspended | cancelled → deleted)
    """

    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    DELETED = "deleted"


class SubscriptionStatus(StrEnum):
    """Estado da assinatura."""

    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    PAUSED = "paused"


class BillingCycle(StrEnum):
    """Ciclo de cobrança."""

    MONTHLY = "monthly"
    YEARLY = "yearly"


class PlanTier(StrEnum):
    """Nível do plano. Define ordenação e hierarquia."""

    STARTER = "starter"
    PRO = "pro"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class DomainType(StrEnum):
    """Tipo de domínio associado ao tenant."""

    SUBDOMAIN = "subdomain"  # tenant.barbeariaos.com.br
    CUSTOM = "custom"  # meudominio.com.br


class MediaType(StrEnum):
    """Tipos de mídia gerenciados pelo tenant."""

    LOGO = "logo"
    LOGO_DARK = "logo_dark"
    FAVICON = "favicon"
    BANNER = "banner"
    GALLERY = "gallery"
    PROFESSIONAL_PHOTO = "professional_photo"
    SERVICE_PHOTO = "service_photo"


class SocialPlatform(StrEnum):
    """Plataformas de redes sociais suportadas."""

    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    TWITTER = "twitter"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"


class DayOfWeek(StrEnum):
    """Dias da semana (Portuguese)."""

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    @property
    def iso_number(self) -> int:
        """0=Monday, 6=Sunday (ISO 8601)."""
        mapping = {
            "monday": 0, "tuesday": 1, "wednesday": 2,
            "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
        }
        return mapping[self.value]


class FeatureFlagTarget(StrEnum):
    """Escopo de feature flag."""

    PLATFORM = "platform"
    TENANT = "tenant"
    PERCENTAGE = "percentage"
