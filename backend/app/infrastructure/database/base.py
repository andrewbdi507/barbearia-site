"""Infrastructure — SQLAlchemy Declarative Base + BaseModel mixin.

Provides:
- Base: SQLAlchemy DeclarativeBase (required for all ORM models)
- BaseModel: Mixin with PK, timestamps, tenant_id, soft delete
- NewBase: Convenience class combining both (recommended for models)
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _new_uuid() -> str:
    return str(uuid4())


class Base(DeclarativeBase):
    """SQLAlchemy declarative base — ALL ORM models MUST inherit from this."""

    pass


class BaseModel:
    """Mixin abstrata com colunas comuns. Use: class SeuModel(Base, BaseModel):"""

    __abstract__ = True
    __allow_unmapped__ = True

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_new_uuid
    )
    tenant_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
