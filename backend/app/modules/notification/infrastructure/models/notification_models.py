"""Notification Module — SQLAlchemy Models."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, BaseModel


class NotificationTemplateModel(Base, BaseModel):
    __tablename__ = "notification_templates"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(20), default="whatsapp")
    language: Mapped[str] = mapped_column(String(10), default="pt-BR")
    version: Mapped[int] = mapped_column(Integer, default=1)
    subject: Mapped[str] = mapped_column(String(500), default="")
    body_template: Mapped[str] = mapped_column(Text, default="")
    variables: Mapped[list] = mapped_column(JSONB, default=list)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="active")
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)

    __table_args__ = (
        UniqueConstraint("tenant_id", "category", "channel", "version", name="uq_tpl_tenant_cat_ch_ver"),
    )


class NotificationModel(Base, BaseModel):
    __tablename__ = "notifications"

    event_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    template_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("notification_templates.id", ondelete="SET NULL"), nullable=True,
    )
    template_version: Mapped[int] = mapped_column(Integer, default=1)
    channel: Mapped[str] = mapped_column(String(20), default="whatsapp", index=True)
    category: Mapped[str] = mapped_column(String(50), index=True)
    priority: Mapped[str] = mapped_column(String(10), default="normal")
    customer_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    recipient_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipient_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    recipient_device_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    subject: Mapped[str] = mapped_column(String(500), default="")
    body: Mapped[str] = mapped_column(Text, default="")
    rendered_content: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    provider_message_id: Mapped[str | None] = mapped_column(String(200), nullable=True, unique=True)
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, default=5)
    next_retry_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    queued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("event_id", "channel", "customer_id", name="uq_notif_event_channel_customer"),
    )


class ChannelConfigModel(Base, BaseModel):
    __tablename__ = "notification_channel_configs"

    channel: Mapped[str] = mapped_column(String(20), default="whatsapp")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    provider: Mapped[str] = mapped_column(String(50), default="")
    credentials_encrypted: Mapped[str] = mapped_column(Text, default="")
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)
    quiet_hours_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    quiet_start: Mapped[str] = mapped_column(String(5), default="22:00")
    quiet_end: Mapped[str] = mapped_column(String(5), default="08:00")

    __table_args__ = (UniqueConstraint("tenant_id", "channel", name="uq_chcfg_tenant_channel"),)
