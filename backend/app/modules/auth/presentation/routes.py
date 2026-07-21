"""Auth Module — API Routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.infrastructure.database.session import get_async_session
from app.modules.auth.application.auth_service import AuthService
from app.modules.auth.application.dto import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    RefreshRequest,
    ResetPasswordRequest,
)
from app.modules.auth.infrastructure.repository import AuthRepository
from app.modules.auth.presentation.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


def _get_service(session: AsyncSession) -> AuthService:
    return AuthService(AuthRepository(session))


# ============================================================
# POST /auth/login
# ============================================================

@router.post("/login")
async def login(
    request: Request,
    body: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Autentica usuário e retorna tokens.

    Access token: corpo da resposta (usado no header Authorization)
    Refresh token: cookie HttpOnly (não acessível via JavaScript)
    """
    service = _get_service(session)
    settings = get_settings()

    tenant_id = body.tenant_id or None

    ip = request.client.host if request.client else None
    ua = request.headers.get("User-Agent")

    user_info, access_token, refresh_token = await service.login(
        email=body.email,
        password=body.password,
        tenant_id=tenant_id,
        ip_address=ip,
        user_agent=ua,
    )

    # Refresh token em cookie HttpOnly
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.app.is_development,
        samesite="strict",
        max_age=settings.security.refresh_token_expire_days * 86400,
        path="/api/v1/auth",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.security.access_token_expire_minutes * 60,
        "user": user_info,
    }


# ============================================================
# POST /auth/refresh
# ============================================================

@router.post("/refresh")
async def refresh_token(
    request: Request,
    response: Response,
    body: RefreshRequest | None = None,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Rotaciona refresh token e retorna novo access token."""
    service = _get_service(session)
    settings = get_settings()

    # Refresh token pode vir do corpo ou do cookie
    token = body.refresh_token if body else None
    if not token:
        token = request.cookies.get("refresh_token")
    if not token:
        from app.core.exceptions import AuthenticationError
        raise AuthenticationError(message="Refresh token não fornecido.")

    access_token, new_refresh = await service.refresh(token)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=not settings.app.is_development,
        samesite="strict",
        max_age=settings.security.refresh_token_expire_days * 86400,
        path="/api/v1/auth",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.security.access_token_expire_minutes * 60,
    }


# ============================================================
# POST /auth/logout
# ============================================================

@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Encerra sessão do usuário."""
    service = _get_service(session)
    refresh_token = request.cookies.get("refresh_token")
    await service.logout(user["user_id"], refresh_token)

    response.delete_cookie("refresh_token", path="/api/v1/auth")
    return {"message": "Logout realizado com sucesso."}


# ============================================================
# POST /auth/logout-all
# ============================================================

@router.post("/logout-all")
async def logout_all(
    response: Response,
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Encerra TODAS as sessões do usuário em todos os dispositivos."""
    service = _get_service(session)
    await service.logout_all(user["user_id"])
    response.delete_cookie("refresh_token", path="/api/v1/auth")
    return {"message": "Todas as sessões foram encerradas."}


# ============================================================
# GET /auth/me
# ============================================================

@router.get("/me")
async def me(
    user: dict = Depends(get_current_user),
) -> dict:
    """Retorna dados do usuário autenticado."""
    return user


# ============================================================
# GET /auth/sessions
# ============================================================

@router.get("/sessions")
async def list_sessions(
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Lista sessões ativas do usuário."""
    service = _get_service(session)
    sessions = await service.get_active_sessions(user["user_id"])
    return {"sessions": sessions}


# ============================================================
# DELETE /auth/sessions/{session_id}
# ============================================================

@router.delete("/sessions/{session_id}")
async def revoke_session(
    session_id: str,
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Revoga uma sessão específica."""
    service = _get_service(session)
    await service.revoke_session(user["user_id"], session_id)
    return {"message": "Sessão revogada."}


# ============================================================
# POST /auth/forgot-password
# ============================================================

@router.post("/forgot-password")
async def forgot_password(
    body: ForgotPasswordRequest,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Solicita recuperação de senha.

    Sempre retorna sucesso (anti-enumeração de usuários).
    O token é enviado por email (integração futura).
    """
    service = _get_service(session)
    token = await service.request_password_reset(body.email, tenant_id="default")

    # No MVP, logar o token (em produção: enviar por email)
    # TODO: Integrar com serviço de email
    return {
        "message": "Se o email existir, enviaremos instruções de recuperação.",
        # "debug_token": token,  # Remover em produção
    }


# ============================================================
# POST /auth/reset-password
# ============================================================

@router.post("/reset-password")
async def reset_password(
    body: ResetPasswordRequest,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Redefine senha usando token de recuperação."""
    service = _get_service(session)
    await service.reset_password(body.token, body.new_password)
    return {"message": "Senha redefinida com sucesso."}


# ============================================================
# POST /auth/change-password
# ============================================================

@router.post("/change-password")
async def change_password(
    body: ChangePasswordRequest,
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Altera senha (usuário autenticado)."""
    service = _get_service(session)
    await service.change_password(user["user_id"], body.current_password, body.new_password)
    return {"message": "Senha alterada com sucesso."}
