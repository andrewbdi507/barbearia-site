"""FastAPI application factory — Barbershop SaaS.

Entry point for the entire platform. Creates and configures
the FastAPI application with all 14 modules, middleware,
and lifecycle events.

Usage:
    uvicorn app.presentation.api.app:create_app --factory
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.infrastructure.database.session import (
    close_session_factory,
    init_session_factory,
)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Application factory — the single entry point for uvicorn.
    Loads all module routers, middleware, and lifecycle handlers.

    Args:
        settings: Optional Settings override (used in tests).

    Returns:
        Fully configured FastAPI application instance.
    """
    if settings is None:
        settings = get_settings()

    app = FastAPI(
        title=settings.app.name,
        version="1.1.0",
        description=(
            "Plataforma SaaS Multi-Tenant para gestão de barbearias "
            "e negócios baseados em agendamento."
        ),
        docs_url="/docs" if settings.app.debug else None,
        redoc_url="/redoc" if settings.app.debug else None,
        openapi_url="/openapi.json" if settings.app.debug else None,
        lifespan=_create_lifespan(settings),
    )

    # ---- Middleware ----
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:3000",
            "https://agendaos-frontend.onrender.com",
            "https://agendaos-site.onrender.com",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )

    # ---- RAW CORS (pure ASGI — cannot fail) ----
    from starlette.types import ASGIApp, Scope, Receive, Send

    class PureCorsMiddleware:
        def __init__(self, app: ASGIApp) -> None:
            self.app = app

        async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
            if scope["type"] == "http":
                async def cors_send(message):
                    if message["type"] == "http.response.start":
                        headers = dict(message.get("headers", []))
                        origin = b"*"
                        for h in scope.get("headers", []):
                            if h[0] == b"origin":
                                origin = h[1]
                                break
                        headers[b"access-control-allow-origin"] = origin
                        headers[b"access-control-allow-credentials"] = b"true"
                        headers[b"access-control-allow-methods"] = b"GET,POST,PUT,PATCH,DELETE,OPTIONS"
                        headers[b"access-control-allow-headers"] = b"*"
                        message["headers"] = list(headers.items())
                    await send(message)

                await self.app(scope, receive, cors_send)
            else:
                await self.app(scope, receive, send)

    app.add_middleware(PureCorsMiddleware)

    # ---- Exception Handlers ----
    _register_exception_handlers(app)

    # ---- Health Check (built-in, no module needed) ----
    @app.get("/health")
    async def health():
        return {"status": "healthy", "version": "1.1.0"}

    @app.get("/health/live")
    async def health_live():
        return {"status": "alive"}

    @app.get("/health/ready")
    async def health_ready():
        return {"status": "ready"}

    # ---- System Health (services dashboard) ----
    from app.presentation.api.health_services import router as health_svc_router
    app.include_router(health_svc_router, prefix="/api/v1")

    # ---- Module Routers ----
    _mount_all_routers(app)

    return app


def _mount_all_routers(app: FastAPI) -> None:
    """Mount all 14 module routers under /api/v1."""
    prefix = "/api/v1"

    # Auth
    from app.modules.auth.presentation.routes import router as auth_router
    from app.modules.auth.presentation.register_routes import register_router
    app.include_router(auth_router, prefix=prefix)
    app.include_router(register_router, prefix=prefix)

    # Tenant
    from app.modules.tenant.presentation.routes import (
        tenant_router,
        plan_router,
    )
    from app.modules.tenant.presentation.saas_routes import saas_router
    app.include_router(tenant_router, prefix=prefix)
    app.include_router(plan_router, prefix=prefix)
    app.include_router(saas_router, prefix=prefix)

    # Staff
    from app.modules.staff.presentation.routes import router as staff_router
    app.include_router(staff_router, prefix=prefix)

    # Scheduling
    from app.modules.scheduling.presentation.routes import router as scheduling_router
    from app.modules.scheduling.presentation.deposit_routes import deposit_router
    app.include_router(scheduling_router, prefix=prefix)
    app.include_router(deposit_router, prefix=f"{prefix}/scheduling")
    from app.modules.scheduling.presentation.deposit_routes import deposit_router
    app.include_router(scheduling_router, prefix=prefix)
    app.include_router(deposit_router, prefix=f"{prefix}/scheduling")

    # Customer / CRM
    from app.modules.customer.presentation.routes import router as customer_router
    app.include_router(customer_router, prefix=prefix)

    # Payment
    from app.modules.payment.presentation.routes import (
        router as payment_router,
        webhook_router,
    )
    app.include_router(payment_router, prefix=prefix)
    app.include_router(webhook_router, prefix=prefix)

    # Notification — register providers + booking automations
    from app.modules.notification.infrastructure.providers import register_providers as reg_notif
    from app.modules.notification.application.booking_automations import register_booking_automations
    reg_notif()
    register_booking_automations()
    from app.modules.notification.presentation.routes import router as notification_router
    app.include_router(notification_router, prefix=prefix)

    # Site (public + admin)
    from app.modules.site.presentation.routes import (
        public_router,
        admin_router,
    )
    app.include_router(public_router, prefix=prefix)
    app.include_router(admin_router, prefix=prefix)

    # Admin Dashboard
    from app.modules.admin.presentation.routes import router as admin_dashboard_router
    app.include_router(admin_dashboard_router, prefix=prefix)

    # Analytics
    from app.modules.analytics.presentation.routes import router as analytics_router
    app.include_router(analytics_router, prefix=prefix)

    # Media / CMS
    from app.modules.media.presentation.routes import router as media_router
    app.include_router(media_router, prefix=prefix)

    # Marketing
    from app.modules.marketing.presentation.routes import router as marketing_router
    app.include_router(marketing_router, prefix=prefix)

    # Agents (Multi-Agent AI Integration)
    from app.presentation.api.agent_routes import agent_router
    app.include_router(agent_router, prefix=prefix)


def _register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers for RFC 7807 error responses."""
    from fastapi import Request
    from fastapi.responses import JSONResponse

    from app.core.exceptions import AppError

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(),
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_error",
                "message": "Erro interno do servidor.",
            },
        )


def _create_lifespan(settings: Settings) -> Any:
    """Create lifespan context manager for startup/shutdown events."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # --- Startup ---
        init_session_factory(settings)

        # --- Yield (app running) ---
        yield

        # --- Shutdown ---
        await close_session_factory()

    return lifespan
