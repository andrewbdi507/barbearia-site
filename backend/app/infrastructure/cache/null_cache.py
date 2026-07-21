"""Null Cache — Fallback quando Redis não está disponível.

Implementa ITenantCache sem cache real.
Usado em desenvolvimento e testes.
"""

from __future__ import annotations

from typing import Any

from app.modules.tenant.domain.interfaces import ITenantCache


class NullTenantCache(ITenantCache):
    """Cache nulo — sempre retorna None (cache miss)."""

    async def get_tenant(self, tenant_id: str) -> dict[str, Any] | None:
        return None

    async def set_tenant(self, tenant_id: str, data: dict[str, Any], ttl: int = 300) -> None:
        pass

    async def get_by_subdomain(self, subdomain: str) -> str | None:
        return None

    async def set_subdomain_mapping(self, subdomain: str, tenant_id: str) -> None:
        pass

    async def get_branding(self, tenant_id: str) -> dict[str, Any] | None:
        return None

    async def set_branding(self, tenant_id: str, data: dict[str, Any], ttl: int = 300) -> None:
        pass

    async def get_settings(self, tenant_id: str) -> dict[str, Any] | None:
        return None

    async def set_settings(self, tenant_id: str, data: dict[str, Any], ttl: int = 300) -> None:
        pass

    async def get_plan(self, plan_id: str) -> dict[str, Any] | None:
        return None

    async def set_plan(self, plan_id: str, data: dict[str, Any], ttl: int = 600) -> None:
        pass

    async def invalidate_tenant(self, tenant_id: str) -> None:
        pass
