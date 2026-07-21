"""System information endpoints.

Provides basic system metadata.
"""

from fastapi import APIRouter

from src.core.config import get_settings

router = APIRouter()


@router.get("/info")
async def system_info() -> dict[str, str]:
    """Return basic system information.

    Non-sensitive metadata about the running application.
    """
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "python_version": __import__("sys").version,
    }


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Simple ping endpoint — minimal overhead."""
    return {"pong": "ok"}
