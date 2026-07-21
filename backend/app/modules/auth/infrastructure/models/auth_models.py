"""Auth Module — SQLAlchemy ORM Models.

Todas as entidades do módulo de autenticação.
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, INET, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.database.base import Base, BaseModel


class UserModel(Base, BaseModel):
    """Usuário do sistema — admin, barbeiro, recepcionista, cliente."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    phone_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_ip: Mapped[str | None] = mapped_column(INET, nullable=True)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    roles: Mapped[list["UserRoleModel"]] = relationship(back_populates="user", lazy="selectin", foreign_keys="[UserRoleModel.user_id]")
    sessions: Mapped[list["SessionModel"]] = relationship(back_populates="user", lazy="selectin")
    refresh_tokens: Mapped[list["RefreshTokenModel"]] = relationship(back_populates="user", lazy="selectin")
    password_resets: Mapped[list["PasswordResetModel"]] = relationship(back_populates="user", lazy="selectin")
    login_logs: Mapped[list["LoginLogModel"]] = relationship(back_populates="user", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("tenant_id", "email", name="uq_users_tenant_email"),
    )


class RoleModel(Base, BaseModel):
    """Papel de usuário com conjunto de permissões."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    permissions: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    users: Mapped[list["UserRoleModel"]] = relationship(back_populates="role", lazy="selectin", foreign_keys="[UserRoleModel.role_id]")


class UserRoleModel(Base, BaseModel):
    """Associação N:N entre User e Role."""

    __tablename__ = "user_roles"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    assigned_by: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=True
    )

    # Relationships
    user: Mapped["UserModel"] = relationship(lazy="selectin", back_populates="roles", foreign_keys=[user_id])
    role: Mapped["RoleModel"] = relationship(lazy="selectin", back_populates="users", foreign_keys=[role_id])


class SessionModel(Base, BaseModel):
    """Sessão ativa de usuário."""

    __tablename__ = "sessions"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    device_info: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    user: Mapped["UserModel"] = relationship(lazy="selectin", back_populates="sessions")


class RefreshTokenModel(Base, BaseModel):
    """Refresh token (opaque) para renovação de access token."""

    __tablename__ = "refresh_tokens"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    family_id: Mapped[str] = mapped_column(UUID(as_uuid=False), default=lambda: str(uuid4()), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped["UserModel"] = relationship(lazy="selectin", back_populates="refresh_tokens")


class PasswordResetModel(Base, BaseModel):
    """Token de recuperação de senha."""

    __tablename__ = "password_resets"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped["UserModel"] = relationship(lazy="selectin", back_populates="password_resets")


class LoginLogModel(Base, BaseModel):
    """Histórico de tentativas de login."""

    __tablename__ = "login_logs"

    user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    email_attempted: Mapped[str] = mapped_column(String(255), nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    failure_reason: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["UserModel | None"] = relationship(lazy="selectin", back_populates="login_logs")
