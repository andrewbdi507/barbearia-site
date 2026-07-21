"""Tenant Module — Redis Cache Implementation.

Implementa ITenantCache para caching de:
- Dados do tenant
- Mapeamento subdomínio → tenant_id
- Branding
- Settings
- Planos
"""

from __future__ import annotations

import json
from typing import Any

from redis.asyncio import Redis as AsyncRedis

from app.modules.tenant.domain.interfaces import ITenantCache


class TenantRedisCache(ITenantCache):
    """Cache Redis para dados de tenant.

    Key patterns:
        tenant:{tenant_id}           → dados completos do tenant
        subdomain:{subdomain}        → tenant_id
        branding:{tenant_id}         → dados de branding
        settings:{tenant_id}         → configurações
        plan:{plan_id}               → dados do plano
    """

    def __init__(self, redis: AsyncRedis, default_ttl: int = 300) -> None:
        self._redis = redis
        self._default_ttl = default_ttl

    # ============================================================
    # Tenant
    # ============================================================

    async def get_tenant(self, tenant_id: str) -> dict[str, Any] | None:
        raw = await self._redis.get(f"tenant:{tenant_id}")
        if raw is None:
            return None
        return json.loads(raw)

    async def set_tenant(self, tenant_id: str, data: dict[str, Any], ttl: int = 300) -> None:
        await self._redis.setex(
            f"tenant:{tenant_id}",
            ttl,
            json.dumps(data, default=str),
        )

    # ============================================================
    # Subdomain → Tenant
    # ============================================================

    async def get_by_subdomain(self, subdomain: str) -> str | None:
        raw = await self._redis.get(f"subdomain:{subdomain.lower()}")
        if raw is None:
            return None
        return raw.decode()

    async def set_subdomain_mapping(self, subdomain: str, tenant_id: str) -> None:
        # Long TTL — raramente muda
        await self._redis.setex(
            f"subdomain:{subdomain.lower()}",
            3600,  # 1 hora
            tenant_id,
        )

    # ============================================================
    # Branding
    # ============================================================

    async def get_branding(self, tenant_id: str) -> dict[str, Any] | None:
        raw = await self._redis.get(f"branding:{tenant_id}")
        if raw is None:
            return None
        return json.loads(raw)

    async def set_branding(self, tenant_id: str, data: dict[str, Any], ttl: int = 300) -> None:
        await self._redis.setex(
            f"branding:{tenant_id}",
            ttl,
            json.dumps(data, default=str),
        )

    # ============================================================
    # Settings
    # ============================================================

    async def get_settings(self, tenant_id: str) -> dict[str, Any] | None:
        raw = await self._redis.get(f"settings:{tenant_id}")
        if raw is None:
            return None
        return json.loads(raw)

    async def set_settings(self, tenant_id: str, data: dict[str, Any], ttl: int = 300) -> None:
        await self._redis.setex(
            f"settings:{tenant_id}",
            ttl,
            json.dumps(data, default=str),
        )

    # ============================================================
    # Plan
    # ============================================================

    async def get_plan(self, plan_id: str) -> dict[str, Any] | None:
        raw = await self._redis.get(f"plan:{plan_id}")
        if raw is None:
            return None
        return json.loads(raw)

    async def set_plan(self, plan_id: str, data: dict[str, Any], ttl: int = 600) -> None:
        await self._redis.setex(
            f"plan:{plan_id}",
            ttl,
            json.dumps(data, default=str),
        )

    # ============================================================
    # Invalidation
    # ============================================================

    async def invalidate_tenant(self, tenant_id: str) -> None:
        """Invalida todo o cache relacionado ao tenant."""
        keys = [
            f"tenant:{tenant_id}",
            f"branding:{tenant_id}",
            f"settings:{tenant_id}",
        ]
        await self._redis.delete(*keys)
