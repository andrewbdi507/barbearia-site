"""Redis cache client.

Provides a simple async Redis client for:
- Session storage
- Rate limiting
- Response caching
- Distributed locks

Uses the redis-py async client.
"""

from __future__ import annotations

from typing import Any

import redis.asyncio as aioredis

from src.core.config import Settings
from src.core.logging import app_logger

logger = app_logger


class RedisClient:
    """Async Redis client wrapper.

    Created once at application startup. Provides typed methods
    for common Redis operations.

    Example:
        redis = RedisClient(settings)
        await redis.connect()
        await redis.set("key", "value", ttl=300)
    """

    def __init__(self, settings: Settings) -> None:
        self._redis_url = settings.redis.url
        self._max_connections = settings.redis.max_connections
        self._client: aioredis.Redis | None = None

    async def connect(self) -> None:
        """Establish connection pool to Redis."""
        self._client = aioredis.from_url(
            self._redis_url,
            max_connections=self._max_connections,
            decode_responses=True,
        )
        # Verify connection
        await self._client.ping()
        logger.info("redis_connected", url=self._redis_url)

    async def disconnect(self) -> None:
        """Close Redis connection pool."""
        if self._client:
            await self._client.close()
            logger.info("redis_disconnected")

    @property
    def client(self) -> aioredis.Redis:
        """Return the underlying Redis client.

        Raises RuntimeError if not connected.
        """
        if self._client is None:
            raise RuntimeError("Redis client not connected. Call connect() first.")
        return self._client

    async def get(self, key: str) -> str | None:
        """Get a value by key."""
        return await self.client.get(key)

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        """Set a key with optional TTL in seconds."""
        await self.client.set(key, value, ex=ttl)

    async def delete(self, *keys: str) -> int:
        """Delete one or more keys."""
        return await self.client.delete(*keys)

    async def exists(self, *keys: str) -> int:
        """Check if keys exist."""
        return await self.client.exists(*keys)

    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter."""
        return await self.client.incrby(key, amount)

    async def expire(self, key: str, ttl: int) -> bool:
        """Set TTL on an existing key."""
        return await self.client.expire(key, ttl)

    async def health_check(self) -> bool:
        """Check if Redis is healthy."""
        try:
            return await self.client.ping()
        except Exception:
            return False


# Module-level singleton
_redis_client: RedisClient | None = None


def init_redis_client(settings: Settings) -> RedisClient:
    """Initialize the global Redis client.

    MUST be called once during application startup.
    """
    global _redis_client
    _redis_client = RedisClient(settings)
    return _redis_client


def get_redis_client() -> RedisClient:
    """Return the current Redis client.

    Raises RuntimeError if not yet initialized.
    """
    if _redis_client is None:
        raise RuntimeError(
            "Redis client not initialized. Call init_redis_client() first."
        )
    return _redis_client
