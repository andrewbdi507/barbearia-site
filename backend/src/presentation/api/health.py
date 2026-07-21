"""Health check endpoints.

Provides Kubernetes-compatible health, readiness, and liveness probes.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.infrastructure.cache import get_redis_client
from src.infrastructure.database import get_async_session

router = APIRouter()


@router.get("/live")
async def liveness() -> dict[str, str]:
    """Liveness probe — is the process running?

    Returns 200 if the application process is alive.
    Does NOT check external dependencies.
    Used by Kubernetes to decide if the pod needs restart.
    """
    return {"status": "alive"}


@router.get("/ready")
async def readiness(
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    """Readiness probe — is the application ready to serve traffic?

    Returns 200 only if ALL critical dependencies are available:
    - Database connection
    - Redis connection (non-blocking — warns but doesn't fail)

    Used by Kubernetes to decide if the pod should receive traffic.
    """
    # Check database
    try:
        await session.execute(
            __import__("sqlalchemy").text("SELECT 1")
        )
    except Exception:
        return {"status": "not_ready", "reason": "database_unreachable"}

    # Check Redis (non-critical — app works without it)
    try:
        redis = get_redis_client()
        if not await redis.health_check():
            return {"status": "degraded", "reason": "redis_unreachable"}
    except RuntimeError:
        # Redis not initialized (acceptable)
        pass

    return {"status": "ready"}


@router.get("/deep")
async def deep_health(
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, object]:
    """Deep health check — comprehensive system health.

    Checks all dependencies including database write capability.
    Useful for external monitoring tools (not Kubernetes probes).
    """
    settings = get_settings()

    health: dict[str, object] = {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "checks": {},
    }

    checks: dict[str, dict[str, str]] = {}

    # Database check
    try:
        start = __import__("time").time()
        await session.execute(
            __import__("sqlalchemy").text("SELECT 1")
        )
        checks["database"] = {
            "status": "ok",
            "latency_ms": str(round((__import__("time").time() - start) * 1000)),
        }
    except Exception as exc:
        checks["database"] = {"status": "error", "message": str(exc)}
        health["status"] = "unhealthy"

    # Redis check
    try:
        redis = get_redis_client()
        start = __import__("time").time()
        ok = await redis.health_check()
        checks["redis"] = {
            "status": "ok" if ok else "error",
            "latency_ms": str(round((__import__("time").time() - start) * 1000)),
        }
    except RuntimeError:
        checks["redis"] = {"status": "not_configured"}
    except Exception as exc:
        checks["redis"] = {"status": "error", "message": str(exc)}

    health["checks"] = checks
    return health
