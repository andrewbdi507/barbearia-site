"""Auth Module — Repository."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.infrastructure.models.auth_models import (
    UserModel,
    RoleModel,
    UserRoleModel,
    SessionModel,
    RefreshTokenModel,
    PasswordResetModel,
    LoginLogModel,
)


class AuthRepository:
    """Repositório para operações de autenticação."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ============================================================
    # User
    # ============================================================

    async def get_user_by_email(self, email: str, tenant_id: str | None = None) -> UserModel | None:
        stmt = select(UserModel).where(
            UserModel.email == email,
            UserModel.deleted_at.is_(None),
        )
        if tenant_id is not None:
            stmt = stmt.where(UserModel.tenant_id == tenant_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: str) -> UserModel | None:
        stmt = select(UserModel).where(
            UserModel.id == user_id,
            UserModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user: UserModel) -> UserModel:
        self._session.add(user)
        await self._session.flush()
        return user

    async def update_user(self, user: UserModel) -> UserModel:
        user.updated_at = datetime.now(timezone.utc)
        await self._session.flush()
        return user

    async def increment_failed_attempts(self, user_id: str) -> int:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(failed_login_attempts=UserModel.failed_login_attempts + 1)
        )
        await self._session.execute(stmt)
        # Retornar contagem atualizada
        result = await self._session.execute(
            select(UserModel.failed_login_attempts).where(UserModel.id == user_id)
        )
        return result.scalar_one()

    async def lock_user(self, user_id: str, until: datetime) -> None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(locked_until=until)
        )
        await self._session.execute(stmt)

    async def reset_failed_attempts(self, user_id: str) -> None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(failed_login_attempts=0, locked_until=None)
        )
        await self._session.execute(stmt)

    async def record_login(self, user_id: str, ip: str | None) -> None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(last_login_at=datetime.now(timezone.utc), last_login_ip=ip)
        )
        await self._session.execute(stmt)

    # ============================================================
    # Roles & Permissions
    # ============================================================

    async def get_user_roles(self, user_id: str) -> list[RoleModel]:
        stmt = (
            select(RoleModel)
            .join(UserRoleModel, UserRoleModel.role_id == RoleModel.id)
            .where(UserRoleModel.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_user_permissions(self, user_id: str) -> list[str]:
        roles = await self.get_user_roles(user_id)
        permissions: set[str] = set()
        for role in roles:
            permissions.update(role.permissions)
        return sorted(permissions)

    async def get_role_by_name(self, name: str, tenant_id: str) -> RoleModel | None:
        stmt = select(RoleModel).where(
            RoleModel.name == name,
            RoleModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_role(self, role: RoleModel) -> RoleModel:
        self._session.add(role)
        await self._session.flush()
        return role

    async def assign_role(self, user_id: str, role_id: str, assigned_by: str | None = None) -> None:
        link = UserRoleModel(user_id=user_id, role_id=role_id, assigned_by=assigned_by)
        self._session.add(link)
        await self._session.flush()

    # ============================================================
    # Sessions
    # ============================================================

    async def create_session(self, session: SessionModel) -> SessionModel:
        self._session.add(session)
        await self._session.flush()
        return session

    async def get_active_sessions(self, user_id: str) -> list[SessionModel]:
        stmt = (
            select(SessionModel)
            .where(
                SessionModel.user_id == user_id,
                SessionModel.is_active.is_(True),
                SessionModel.expires_at > datetime.now(timezone.utc),
            )
            .order_by(SessionModel.last_activity_at.desc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def revoke_session(self, session_id: str) -> None:
        stmt = (
            update(SessionModel)
            .where(SessionModel.id == session_id)
            .values(is_active=False)
        )
        await self._session.execute(stmt)

    async def revoke_all_sessions(self, user_id: str) -> None:
        stmt = (
            update(SessionModel)
            .where(SessionModel.user_id == user_id, SessionModel.is_active.is_(True))
            .values(is_active=False)
        )
        await self._session.execute(stmt)

    # ============================================================
    # Refresh Tokens
    # ============================================================

    async def create_refresh_token(self, token: RefreshTokenModel) -> RefreshTokenModel:
        self._session.add(token)
        await self._session.flush()
        return token

    async def get_refresh_token(self, token_hash: str) -> RefreshTokenModel | None:
        stmt = select(RefreshTokenModel).where(
            RefreshTokenModel.token_hash == token_hash,
            RefreshTokenModel.is_revoked.is_(False),
            RefreshTokenModel.expires_at > datetime.now(timezone.utc),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke_refresh_token(self, token_hash: str) -> None:
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.token_hash == token_hash)
            .values(is_revoked=True, revoked_at=datetime.now(timezone.utc))
        )
        await self._session.execute(stmt)

    async def revoke_token_family(self, family_id: str) -> None:
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.family_id == family_id)
            .values(is_revoked=True, revoked_at=datetime.now(timezone.utc))
        )
        await self._session.execute(stmt)

    # ============================================================
    # Password Reset
    # ============================================================

    async def create_password_reset(self, reset: PasswordResetModel) -> PasswordResetModel:
        self._session.add(reset)
        await self._session.flush()
        return reset

    async def get_valid_reset_token(self, token_hash: str) -> PasswordResetModel | None:
        stmt = select(PasswordResetModel).where(
            PasswordResetModel.token_hash == token_hash,
            PasswordResetModel.used_at.is_(None),
            PasswordResetModel.expires_at > datetime.now(timezone.utc),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def mark_reset_used(self, token_hash: str) -> None:
        stmt = (
            update(PasswordResetModel)
            .where(PasswordResetModel.token_hash == token_hash)
            .values(used_at=datetime.now(timezone.utc))
        )
        await self._session.execute(stmt)

    # ============================================================
    # Login Logs
    # ============================================================

    async def log_login_attempt(self, log: LoginLogModel) -> None:
        self._session.add(log)
        await self._session.flush()

    async def get_recent_failed_attempts(self, email: str, minutes: int = 15) -> int:
        since = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        stmt = select(func.count()).where(
            LoginLogModel.email_attempted == email,
            LoginLogModel.success.is_(False),
            LoginLogModel.created_at >= since,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()
