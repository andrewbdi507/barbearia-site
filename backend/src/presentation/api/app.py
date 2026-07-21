"""FastAPI application factory.

Creates and configures the FastAPI application with:
- Middleware stack (CORS, security headers, request ID, rate limiting)
- Exception handlers (RFC 7807)
- Health check endpoints
- API router mounting
- OpenAPI documentation
- Lifecycle events (startup/shutdown)
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.core.config import Settings, get_settings
from src.core.logging import setup_logging, app_logger
from src.infrastructure.cache import init_redis_client
from src.infrastructure.database import init_session_factory
from src.presentation.api.routes import router as api_router
from src.presentation.middleware.error_handler import register_exception_handlers
from src.presentation.middleware.request_id import RequestIDMiddleware
from src.presentation.middleware.security_headers import SecurityHeadersMiddleware

logger = app_logger


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    This is the application factory — the single entry point
    for creating the FastAPI instance. Used by uvicorn with --factory.

    Args:
        settings: Optional Settings override (used in tests).

    Returns:
        A fully configured FastAPI application.
    """
    if settings is None:
        settings = get_settings()

    # Initialize logging first
    setup_logging()

    # Create FastAPI instance
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Plataforma SaaS Multi-Tenant para gestão de barbearias",
        docs_url="/docs" if settings.app_debug else None,
        redoc_url="/redoc" if settings.app_debug else None,
        openapi_url="/openapi.json" if settings.app_debug else None,
        lifespan=_create_lifespan(settings),
    )

    # ---- Middleware (order matters!) ----
    # 1. Request ID — must be first to propagate to all downstream
    app.add_middleware(RequestIDMiddleware)

    # 2. Security headers
    app.add_middleware(SecurityHeadersMiddleware)

    # 3. CORS — explicit origins only
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )

    # ---- Exception Handlers ----
    register_exception_handlers(app)

    # ---- Routes ----
    app.include_router(api_router)

    # ---- Custom OpenAPI Schema ----
    _customize_openapi(app, settings)

    logger.info(
        "app_created",
        app_name=settings.app_name,
        app_env=settings.app_env,
        debug=settings.app_debug,
    )

    return app


def _create_lifespan(settings: Settings) -> Any:
    """Create the application lifespan context manager.

    Handles startup (init DB, Redis) and shutdown (cleanup).
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> Any:
        # Startup
        logger.info("app_starting", env=settings.app_env)

        # Initialize database session factory
        init_session_factory(settings)
        logger.info("database_initialized")

        # Initialize Redis (non-critical — app works without it)
        try:
            redis = init_redis_client(settings)
            await redis.connect()
        except Exception as exc:
            logger.warning("redis_unavailable", error=str(exc))

        logger.info("app_started", env=settings.app_env)
        yield
        # Shutdown
        logger.info("app_shutting_down")

        from src.infrastructure.database import get_session_factory

        try:
            factory = get_session_factory()
            await factory.dispose()
        except RuntimeError:
            pass  # Not initialized (shouldn't happen)

        from src.infrastructure.cache import get_redis_client

        try:
            redis = get_redis_client()
            await redis.disconnect()
        except RuntimeError:
            pass

        logger.info("app_stopped")

    return lifespan


def _customize_openapi(app: FastAPI, _settings: Settings) -> None:
    """Add custom OpenAPI schema metadata."""

    def custom_openapi() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # Add security schemes
        openapi_schema.setdefault("components", {})
        openapi_schema["components"].setdefault("securitySchemes", {})
        openapi_schema["components"]["securitySchemes"] = {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT access token obtained via /auth/login",
            }
        }

        # Add tags metadata
        openapi_schema.setdefault("tags", [])
        openapi_schema["tags"].extend(
            [
                {"name": "health", "description": "Health check endpoints"},
                {"name": "system", "description": "System information"},
            ]
        )

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore[method-assign]
