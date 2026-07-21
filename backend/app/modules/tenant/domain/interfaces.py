"""Tenant Module — Repository Interfaces (Ports).

Define os contratos que a camada de infrastructure deve implementar.
Seguindo o Dependency Inversion Principle: domain define, infrastructure implementa.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

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


class ITenantRepository(ABC):
    """Contrato para persistência de Tenant."""

    @abstractmethod
    async def get_by_id(self, tenant_id: str) -> Tenant | None: ...

    @abstractmethod
    async def get_by_subdomain(self, subdomain: str) -> Tenant | None: ...

    @abstractmethod
    async def get_by_domain(self, domain_name: str) -> Tenant | None: ...

    @abstractmethod
    async def list_all(
        self, *, status: str | None = None, offset: int = 0, limit: int = 50
    ) -> tuple[list[Tenant], int]: ...

    @abstractmethod
    async def create(self, tenant: Tenant) -> Tenant: ...

    @abstractmethod
    async def update(self, tenant: Tenant) -> Tenant: ...

    @abstractmethod
    async def soft_delete(self, tenant_id: str) -> None: ...

    @abstractmethod
    async def update_status(self, tenant_id: str, status: str, reason: str | None = None) -> None: ...

    @abstractmethod
    async def subdomain_exists(self, subdomain: str, exclude_id: str | None = None) -> bool: ...

    @abstractmethod
    async def get_usage_counts(self, tenant_id: str) -> dict[str, int]: ...


class IPlanRepository(ABC):
    """Contrato para persistência de Plan."""

    @abstractmethod
    async def get_by_id(self, plan_id: str) -> Plan | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Plan | None: ...

    @abstractmethod
    async def list_active(self) -> list[Plan]: ...

    @abstractmethod
    async def list_all(self) -> list[Plan]: ...

    @abstractmethod
    async def create(self, plan: Plan) -> Plan: ...

    @abstractmethod
    async def update(self, plan: Plan) -> Plan: ...


class ISubscriptionRepository(ABC):
    """Contrato para persistência de Subscription."""

    @abstractmethod
    async def get_by_id(self, subscription_id: str) -> Subscription | None: ...

    @abstractmethod
    async def get_active_for_tenant(self, tenant_id: str) -> Subscription | None: ...

    @abstractmethod
    async def get_history_for_tenant(self, tenant_id: str) -> list[Subscription]: ...

    @abstractmethod
    async def create(self, subscription: Subscription) -> Subscription: ...

    @abstractmethod
    async def update(self, subscription: Subscription) -> Subscription: ...

    @abstractmethod
    async def update_status(self, subscription_id: str, status: str) -> None: ...


class ITenantSettingsRepository(ABC):
    """Contrato para persistência de TenantSettings."""

    @abstractmethod
    async def get_for_tenant(self, tenant_id: str) -> TenantSettings | None: ...

    @abstractmethod
    async def upsert(self, settings: TenantSettings) -> TenantSettings: ...


class ITenantBrandingRepository(ABC):
    """Contrato para persistência de TenantBranding."""

    @abstractmethod
    async def get_for_tenant(self, tenant_id: str) -> TenantBranding | None: ...

    @abstractmethod
    async def upsert(self, branding: TenantBranding) -> TenantBranding: ...


class IBusinessHoursRepository(ABC):
    """Contrato para persistência de BusinessHours."""

    @abstractmethod
    async def get_for_tenant(self, tenant_id: str) -> list[BusinessHours]: ...

    @abstractmethod
    async def upsert_batch(self, tenant_id: str, hours: list[BusinessHours]) -> list[BusinessHours]: ...


class IDomainRepository(ABC):
    """Contrato para persistência de Domain."""

    @abstractmethod
    async def get_for_tenant(self, tenant_id: str) -> list[Domain]: ...

    @abstractmethod
    async def get_by_name(self, domain_name: str) -> Domain | None: ...

    @abstractmethod
    async def create(self, domain: Domain) -> Domain: ...

    @abstractmethod
    async def delete(self, domain_id: str) -> None: ...


class ISocialMediaRepository(ABC):
    """Contrato para persistência de SocialMedia."""

    @abstractmethod
    async def get_for_tenant(self, tenant_id: str) -> list[SocialMedia]: ...

    @abstractmethod
    async def upsert_batch(self, tenant_id: str, links: list[SocialMedia]) -> list[SocialMedia]: ...


class ITenantMediaRepository(ABC):
    """Contrato para persistência de TenantMedia."""

    @abstractmethod
    async def get_for_tenant(
        self, tenant_id: str, media_type: str | None = None
    ) -> list[TenantMedia]: ...

    @abstractmethod
    async def create(self, media: TenantMedia) -> TenantMedia: ...

    @abstractmethod
    async def delete(self, media_id: str) -> None: ...


class IFeatureFlagRepository(ABC):
    """Contrato para persistência de FeatureFlag."""

    @abstractmethod
    async def get_by_name(self, name: str) -> FeatureFlag | None: ...

    @abstractmethod
    async def is_enabled(self, name: str, tenant_id: str) -> bool: ...


class ITenantCache(ABC):
    """Contrato para cache de dados do tenant."""

    @abstractmethod
    async def get_tenant(self, tenant_id: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def set_tenant(self, tenant_id: str, data: dict[str, Any], ttl: int = 300) -> None: ...

    @abstractmethod
    async def get_by_subdomain(self, subdomain: str) -> str | None: ...

    @abstractmethod
    async def set_subdomain_mapping(self, subdomain: str, tenant_id: str) -> None: ...

    @abstractmethod
    async def get_branding(self, tenant_id: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def set_branding(self, tenant_id: str, data: dict[str, Any], ttl: int = 300) -> None: ...

    @abstractmethod
    async def get_settings(self, tenant_id: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def set_settings(self, tenant_id: str, data: dict[str, Any], ttl: int = 300) -> None: ...

    @abstractmethod
    async def get_plan(self, plan_id: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def set_plan(self, plan_id: str, data: dict[str, Any], ttl: int = 600) -> None: ...

    @abstractmethod
    async def invalidate_tenant(self, tenant_id: str) -> None: ...
