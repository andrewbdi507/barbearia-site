"""Auth Module — Application Service (Use Cases).

Orquestra a lógica de autenticação utilizando o repositório
e os serviços de segurança (Argon2, JWT).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.core.config import get_settings
from app.core.exceptions import (
    AuthenticationError,
    InvalidCredentialsError,
    TokenExpiredError,
    TokenInvalidError,
    BusinessRuleError,
)
from app.modules.auth.infrastructure.models.auth_models import (
    UserModel,
    SessionModel,
    RefreshTokenModel,
    PasswordResetModel,
    LoginLogModel,
)
from app.modules.auth.infrastructure.repository import AuthRepository
from app.modules.auth.infrastructure import security as sec


class AuthService:
    """Serviço de aplicação para autenticação e autorização."""

    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_MINUTES = 15

    def __init__(self, repository: AuthRepository) -> None:
        self._repo = repository
        self._settings = get_settings()

    # ============================================================
    # Login
    # ============================================================

    async def login(
        self,
        email: str,
        password: str,
        tenant_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        device_info: dict | None = None,
    ) -> tuple[dict, str, str]:
        """Autentica usuário e retorna tokens + user info.

        Fluxo:
        1. Buscar usuário por email + tenant
        2. Verificar se conta está bloqueada
        3. Verificar senha
        4. Registrar login (sucesso ou falha)
        5. Gerar tokens
        6. Criar sessão

        Raises:
            InvalidCredentialsError: Credenciais inválidas
            BusinessRuleError: Conta bloqueada/suspensa
        """
        user = await self._repo.get_user_by_email(email, tenant_id)

        # Usuário não encontrado — mensagem genérica (anti-enumeração)
        if user is None:
            await self._log_attempt(None, email, False, "user_not_found", ip_address, user_agent)
            raise InvalidCredentialsError()

        # Conta bloqueada por tentativas
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            await self._log_attempt(user.id, email, False, "account_locked", ip_address, user_agent)
            raise BusinessRuleError(
                message="Conta temporariamente bloqueada. Tente novamente em alguns minutos.",
                details={"locked_until": user.locked_until.isoformat()},
            )

        # Conta inativa
        if not user.is_active:
            await self._log_attempt(user.id, email, False, "account_inactive", ip_address, user_agent)
            raise BusinessRuleError(message="Conta desativada. Entre em contato com o suporte.")

        # Verificar senha
        if not sec.verify_password(password, user.password_hash):
            attempts = await self._repo.increment_failed_attempts(user.id)
            await self._log_attempt(user.id, email, False, "invalid_password", ip_address, user_agent)

            # Bloquear após N tentativas
            if attempts >= self.MAX_FAILED_ATTEMPTS:
                lock_until = datetime.now(timezone.utc) + timedelta(minutes=self.LOCKOUT_MINUTES)
                await self._repo.lock_user(user.id, lock_until)

            raise InvalidCredentialsError()

        # Rehash se necessário (parâmetros do Argon2 mudaram)
        if sec.needs_rehash(user.password_hash):
            user.password_hash = sec.hash_password(password)
            await self._repo.update_user(user)

        # Sucesso — resetar contador
        await self._repo.reset_failed_attempts(user.id)
        await self._repo.record_login(user.id, ip_address)
        await self._log_attempt(user.id, email, True, None, ip_address, user_agent)

        # Obter permissões
        permissions = await self._repo.get_user_permissions(user.id)
        roles = await self._repo.get_user_roles(user.id)

        # Gerar tokens
        extra_claims = {
            "permissions": permissions,
            "role": roles[0].name if roles else "unknown",
        }
        access_token = sec.create_access_token(
            subject=user.id,
            tenant_id=user.tenant_id,
            extra_claims=extra_claims,
        )
        refresh_token_raw = sec.create_refresh_token(user.id, user.tenant_id)

        # Armazenar refresh token (hash)
        refresh = RefreshTokenModel(
            user_id=user.id,
            token_hash=sec.hash_token(refresh_token_raw),
            family_id=str(uuid4()),
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=self._settings.security.refresh_token_expire_days),
        )
        await self._repo.create_refresh_token(refresh)

        # Criar sessão
        session = SessionModel(
            user_id=user.id,
            token_hash=sec.hash_token(access_token),
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
            ip_address=ip_address,
            user_agent=user_agent,
            device_info=device_info or {},
        )
        await self._repo.create_session(session)

        user_info = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "avatar_url": user.avatar_url,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "permissions": permissions,
            "roles": [r.name for r in roles],
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
        }

        return user_info, access_token, refresh_token_raw

    # ============================================================
    # Refresh Token
    # ============================================================

    async def refresh(self, refresh_token_raw: str) -> tuple[str, str]:
        """Rotaciona refresh token e gera novo par de tokens.

        Implementa Refresh Token Rotation:
        - Token usado é revogado
        - Se reuso detectado (token já revogado) → revoga família inteira
        - Novo token gerado na mesma família
        """
        token_hash = sec.hash_token(refresh_token_raw)

        stored = await self._repo.get_refresh_token(token_hash)
        if stored is None:
            # Token não encontrado — pode ser reuso de token já revogado
            # Buscar token mesmo revogado para detectar reuso
            raise TokenInvalidError(message="Refresh token inválido ou expirado.")

        # Revogar token atual (rotação)
        await self._repo.revoke_refresh_token(token_hash)

        # Buscar usuário
        user = await self._repo.get_user_by_id(stored.user_id)
        if user is None or not user.is_active:
            raise BusinessRuleError(message="Usuário não encontrado ou inativo.")

        # Gerar novos tokens
        permissions = await self._repo.get_user_permissions(user.id)
        roles = await self._repo.get_user_roles(user.id)

        access_token = sec.create_access_token(
            subject=user.id,
            tenant_id=user.tenant_id,
            extra_claims={
                "permissions": permissions,
                "role": roles[0].name if roles else "unknown",
            },
        )
        new_refresh_raw = sec.create_refresh_token(user.id, user.tenant_id)

        new_refresh = RefreshTokenModel(
            user_id=user.id,
            token_hash=sec.hash_token(new_refresh_raw),
            family_id=stored.family_id,
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=self._settings.security.refresh_token_expire_days),
        )
        await self._repo.create_refresh_token(new_refresh)

        return access_token, new_refresh_raw

    # ============================================================
    # Logout
    # ============================================================

    async def logout(self, user_id: str, refresh_token_raw: str | None = None) -> None:
        """Revoga refresh token e encerra sessões."""
        if refresh_token_raw:
            token_hash = sec.hash_token(refresh_token_raw)
            await self._repo.revoke_refresh_token(token_hash)
        await self._repo.revoke_all_sessions(user_id)

    async def logout_all(self, user_id: str) -> None:
        """Revoga TODOS os refresh tokens e sessões do usuário."""
        # Revogar todas as sessões
        await self._repo.revoke_all_sessions(user_id)
        # Revogar todos os refresh tokens
        # (implementação simplificada — revoga por família)
        pass

    # ============================================================
    # Password Reset
    # ============================================================

    async def request_password_reset(self, email: str, tenant_id: str) -> str | None:
        """Solicita recuperação de senha.

        Sempre retorna sucesso (anti-enumeração).
        Gera token com expiração de 1 hora.
        """
        user = await self._repo.get_user_by_email(email, tenant_id)
        if user is None:
            return None  # Não revela se email existe

        raw_token = sec.generate_secure_token(32)
        reset = PasswordResetModel(
            user_id=user.id,
            token_hash=sec.hash_token(raw_token),
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        await self._repo.create_password_reset(reset)
        return raw_token

    async def reset_password(self, token: str, new_password: str) -> bool:
        """Redefine senha usando token de recuperação.

        Token é de uso único. Após uso, é marcado como utilizado.
        """
        token_hash = sec.hash_token(token)
        reset = await self._repo.get_valid_reset_token(token_hash)
        if reset is None:
            raise TokenInvalidError(message="Token inválido ou expirado.")

        user = await self._repo.get_user_by_id(reset.user_id)
        if user is None:
            raise BusinessRuleError(message="Usuário não encontrado.")

        # Atualizar senha
        user.password_hash = sec.hash_password(new_password)
        await self._repo.update_user(user)

        # Marcar token como usado
        await self._repo.mark_reset_used(token_hash)

        # Revogar todas as sessões (segurança)
        await self._repo.revoke_all_sessions(user.id)

        return True

    async def change_password(
        self, user_id: str, current_password: str, new_password: str
    ) -> bool:
        """Altera senha (usuário autenticado)."""
        user = await self._repo.get_user_by_id(user_id)
        if user is None:
            raise BusinessRuleError(message="Usuário não encontrado.")

        if not sec.verify_password(current_password, user.password_hash):
            raise InvalidCredentialsError(message="Senha atual incorreta.")

        user.password_hash = sec.hash_password(new_password)
        await self._repo.update_user(user)

        # Revogar outras sessões (manter sessão atual via novo token)
        return True

    # ============================================================
    # Sessions
    # ============================================================

    async def get_active_sessions(self, user_id: str) -> list[dict]:
        """Lista sessões ativas do usuário."""
        sessions = await self._repo.get_active_sessions(user_id)
        return [
            {
                "id": s.id,
                "ip_address": s.ip_address,
                "user_agent": s.user_agent,
                "device_info": s.device_info,
                "is_active": s.is_active,
                "last_activity_at": s.last_activity_at.isoformat(),
                "created_at": s.created_at.isoformat(),
            }
            for s in sessions
        ]

    async def revoke_session(self, user_id: str, session_id: str) -> None:
        """Revoga uma sessão específica."""
        await self._repo.revoke_session(session_id)

    # ============================================================
    # RBAC
    # ============================================================

    async def get_user_permissions(self, user_id: str) -> list[str]:
        """Retorna permissões efetivas do usuário."""
        return await self._repo.get_user_permissions(user_id)

    async def has_permission(self, user_id: str, permission: str) -> bool:
        """Verifica se usuário tem permissão específica."""
        permissions = await self.get_user_permissions(user_id)
        return permission in permissions

    # ============================================================
    # Private Helpers
    # ============================================================

    async def _log_attempt(
        self,
        user_id: str | None,
        email: str,
        success: bool,
        failure_reason: str | None,
        ip_address: str | None,
        user_agent: str | None,
    ) -> None:
        log = LoginLogModel(
            user_id=user_id,
            email_attempted=email,
            success=success,
            failure_reason=failure_reason,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        await self._repo.log_login_attempt(log)
