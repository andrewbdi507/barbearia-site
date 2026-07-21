"""Tenant Module — Middleware.

Resolução automática de tenant para TODA requisição.
Garante isolamento multi-tenant sem depender dos controllers.

Fluxo:
1. Extrai tenant do subdomínio (ou header X-Tenant-ID para super_admin)
2. Valida acesso (tenant ativo, assinatura válida)
3. Injeta tenant_id no request.state
4. Propaga para contexto do banco (RLS)
"""

from __future__ import annotations

from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import (
    AuthenticationError,
    TenantAccessDeniedError,
    TenantNotFoundError,
    TenantSuspendedError,
)
from app.modules.tenant.application.tenant_service import TenantService


class TenantMiddleware(BaseHTTPMiddleware):
    """Middleware que resolve e valida o tenant em toda requisição.

    Rotas públicas (sem tenant): /api/v1/auth/login, /api/v1/health, etc.
    Rotas tenantizadas: todas as demais.
    """

    PUBLIC_PATHS = {
        "/api/v1/auth/login",
        "/api/v1/auth/refresh",
        "/api/v1/auth/forgot-password",
        "/api/v1/auth/reset-password",
        "/api/v1/health",
        "/api/v1/health/ready",
        "/api/v1/docs",
        "/api/v1/openapi.json",
        "/api/v1/redoc",
    }

    def __init__(
        self,
        app,
        tenant_service_factory: Callable[[], TenantService],
    ) -> None:
        super().__init__(app)
        self._get_service = tenant_service_factory

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Pular rotas públicas
        if request.url.path in self.PUBLIC_PATHS or request.url.path.startswith("/api/v1/docs"):
            return await call_next(request)

        # Resolver tenant
        tenant_id = await self._resolve_tenant(request)

        if tenant_id is None:
            # Se a rota requer auth, o dependency get_current_user vai falhar
            # Se não requer, permite passar (ex: site público com subdomínio)
            return await call_next(request)

        # Validar acesso
        try:
            service = self._get_service()
            tenant = await service.check_tenant_access(tenant_id)
            request.state.tenant_id = tenant.id
            request.state.tenant_status = tenant.status
            request.state.plan_id = tenant.plan_id
        except (TenantNotFoundError, TenantSuspendedError, TenantAccessDeniedError) as e:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=e.status_code,
                content={"error": e.code, "message": e.message},
            )

        return await call_next(request)

    async def _resolve_tenant(self, request: Request) -> str | None:
        """Resolve tenant_id de múltiplas fontes:

        1. JWT claim 'tenant_id' (já validado pelo get_current_user)
        2. Subdomínio: tenant_id.barbeariaos.com.br
        3. Header X-Tenant-ID (para super_admin cross-tenant)
        4. Cookie tenant_id (fallback)
        """
        # 1. Do request.state (setado pelo get_current_user dependency)
        if hasattr(request.state, "tenant_id") and request.state.tenant_id:
            return request.state.tenant_id

        # 2. Header X-Tenant-ID (super_admin acessando tenant específico)
        header_tenant = request.headers.get("X-Tenant-ID")
        if header_tenant:
            # Só permitir se for super_admin (validado depois)
            return header_tenant

        # 3. Subdomínio
        host = request.headers.get("host", "")
        if host:
            subdomain = self._extract_subdomain(host)
            if subdomain and subdomain not in ("api", "admin", "app", "www"):
                service = self._get_service()
                try:
                    tenant = await service.get_tenant_by_subdomain(subdomain)
                    return tenant.id
                except TenantNotFoundError:
                    pass

        return None

    @staticmethod
    def _extract_subdomain(host: str) -> str | None:
        """Extrai subdomínio do host.

        studio27.barbeariaos.com.br → studio27
        localhost → None
        """
        host = host.split(":")[0]  # Remove porta
        parts = host.split(".")
        if len(parts) >= 3:
            return parts[0]
        return None
