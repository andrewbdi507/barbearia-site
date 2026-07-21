"""Auth Module — FastAPI Dependencies.

Fornece dependências injetáveis para autenticação e autorização:
- get_current_user: Extrai e valida JWT do header Authorization
- require_permissions: Verifica permissões RBAC
- require_tenant: Valida isolamento multi-tenant
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Cookie, Depends, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError, AuthorizationError, TenantAccessDeniedError
from app.infrastructure.database.session import get_async_session
from app.modules.auth.infrastructure.repository import AuthRepository
from app.modules.auth.infrastructure.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Extrai e valida o usuário atual do JWT.

    Usado como dependência em rotas protegidas.
    Injeta user_id, tenant_id, permissions no request.state.

    Raises:
        AuthenticationError: Token ausente, inválido ou expirado.
    """
    token = None

    # 1. Tentar header Authorization: Bearer <token>
    if credentials:
        token = credentials.credentials

    # 2. Tentar cookie access_token (fallback para web)
    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise AuthenticationError(message="Token de acesso não fornecido.")

    try:
        payload = decode_token(token)
    except Exception:
        raise AuthenticationError(message="Token inválido ou expirado.")

    if payload.get("type") != "access":
        raise AuthenticationError(message="Tipo de token inválido.")

    user_id = payload["sub"]
    tenant_id = payload.get("tenant_id")

    # Verificar se usuário ainda existe e está ativo
    repo = AuthRepository(session)
    user = await repo.get_user_by_id(user_id)
    if user is None or not user.is_active:
        raise AuthenticationError(message="Usuário não encontrado ou inativo.")

    # Verificar se tenant ainda está ativo (aqui pode chamar TenantRepository)

    # Injeta no request.state para uso em middlewares/rotas
    request.state.user_id = user_id
    request.state.tenant_id = tenant_id
    request.state.permissions = payload.get("permissions", [])
    request.state.role = payload.get("role", "unknown")

    return {
        "user_id": user_id,
        "tenant_id": tenant_id,
        "email": user.email,
        "name": user.name,
        "permissions": payload.get("permissions", []),
        "role": payload.get("role", "unknown"),
    }


def require_permissions(*required: str):
    """Factory de dependência: verifica permissões RBAC.

    Uso:
        @router.get("/admin")
        async def admin_route(
            user: Annotated[dict, Depends(require_permissions("admin:access"))]
        ):
            ...

    Raises:
        AuthorizationError: Usuário não tem as permissões necessárias.
    """

    async def checker(
        request: Request,
        user: dict = Depends(get_current_user),
    ) -> dict:
        permissions: list[str] = user.get("permissions", [])
        missing = [p for p in required if p not in permissions]
        if missing:
            raise AuthorizationError(
                message="Permissões insuficientes.",
                details={"required": list(required), "missing": missing},
            )
        return user

    return checker


async def require_tenant_match(
    request: Request,
    tenant_id_from_path: str,
    user: dict = Depends(get_current_user),
) -> dict:
    """Valida que o usuário pertence ao tenant do recurso acessado.

    Previne cross-tenant access (IDOR entre tenants).
    """
    user_tenant = user.get("tenant_id")
    if user_tenant and user_tenant != tenant_id_from_path:
        raise TenantAccessDeniedError(
            details={"user_tenant": user_tenant, "requested_tenant": tenant_id_from_path}
        )
    return user
