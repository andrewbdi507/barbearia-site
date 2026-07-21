"""Tenant Module — Value Objects.

Objetos de valor imutáveis — comparados por atributos, não por identidade.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Subdomain:
    """Subdomínio validado: apenas [a-z0-9-], 3-63 chars."""

    value: str

    PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]{1,61}[a-z0-9])?$")

    def __post_init__(self) -> None:
        if not self.PATTERN.match(self.value):
            raise ValueError(
                f"Subdomínio inválido: '{self.value}'. "
                f"Use apenas letras minúsculas, números e hífens (3-63 chars)."
            )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class PlanLimits:
    """Limites de recursos de um plano (imutável, configurável no banco).

    Cada valor 0 = ilimitado.
    """

    max_professionals: int = 5
    max_customers: int = 500
    max_bookings_per_month: int = 200
    max_users: int = 5
    max_integrations: int = 0  # 0 = nenhuma
    max_notifications_per_month: int = 500
    max_upload_storage_mb: int = 100
    max_gallery_photos: int = 10
    custom_domain: bool = False
    custom_branding: bool = False
    reports_advanced: bool = False
    whatsapp_integration: bool = False
    api_access: bool = False
    priority_support: bool = False

    def to_dict(self) -> dict[str, int | bool]:
        return {
            "max_professionals": self.max_professionals,
            "max_customers": self.max_customers,
            "max_bookings_per_month": self.max_bookings_per_month,
            "max_users": self.max_users,
            "max_integrations": self.max_integrations,
            "max_notifications_per_month": self.max_notifications_per_month,
            "max_upload_storage_mb": self.max_upload_storage_mb,
            "max_gallery_photos": self.max_gallery_photos,
            "custom_domain": self.custom_domain,
            "custom_branding": self.custom_branding,
            "reports_advanced": self.reports_advanced,
            "whatsapp_integration": self.whatsapp_integration,
            "api_access": self.api_access,
            "priority_support": self.priority_support,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PlanLimits:
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in valid_keys})


@dataclass(frozen=True, slots=True)
class BusinessHoursSlot:
    """Faixa de horário de funcionamento para um dia."""

    day_of_week: int  # 0=Monday, 6=Sunday (ISO)
    open_time: str  # "HH:MM"
    close_time: str  # "HH:MM"
    is_closed: bool = False
    lunch_start: str | None = None
    lunch_end: str | None = None
    slot_duration_minutes: int = 30

    def __post_init__(self) -> None:
        if not 0 <= self.day_of_week <= 6:
            raise ValueError(f"Dia inválido: {self.day_of_week}")


@dataclass(frozen=True, slots=True)
class BrandingColors:
    """Paleta de cores do tenant."""

    primary: str = "#1a1a2e"
    primary_hover: str = "#16213e"
    secondary: str = "#e94560"
    background: str = "#f5f5f5"
    surface: str = "#ffffff"
    text: str = "#333333"
    text_light: str = "#666666"
    success: str = "#27ae60"
    error: str = "#e74c3c"
    warning: str = "#f39c12"

    HEX_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")

    def __post_init__(self) -> None:
        for field_name in self.__dataclass_fields__:
            val = getattr(self, field_name)
            if not self.HEX_PATTERN.match(val):
                raise ValueError(f"Cor inválida '{field_name}': {val}")
