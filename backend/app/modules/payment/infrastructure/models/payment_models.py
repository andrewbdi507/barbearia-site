"""Payment Module — SQLAlchemy Models.

4 modelos: Payment, PaymentEvent, GatewayConfig, SubscriptionPayment.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, BaseModel


class PaymentModel(Base, BaseModel):
    __tablename__ = "payments"

    booking_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    subscription_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    customer_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    amount: Mapped[int] = mapped_column(Integer, default=0)
    original_amount: Mapped[int] = mapped_column(Integer, default=0)
    currency: Mapped[str] = mapped_column(String(5), default="BRL")
    status: Mapped[str] = mapped_column(String(30), default="pending", index=True)
    payment_method: Mapped[str | None] = mapped_column(String(20), nullable=True)
    gateway: Mapped[str] = mapped_column(String(30), default="mercado_pago")
    gateway_payment_id: Mapped[str | None] = mapped_column(String(200), nullable=True, unique=True, index=True)
    gateway_checkout_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    pix_qr_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    pix_copy_paste: Mapped[str | None] = mapped_column(Text, nullable=True)
    pix_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=True, index=True)
    deposit_type: Mapped[str] = mapped_column(String(20), default="none")
    deposit_value: Mapped[int] = mapped_column(Integer, default=0)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    refunded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    refunded_amount: Mapped[int] = mapped_column(Integer, default=0)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)

    events: Mapped[list["PaymentEventModel"]] = relationship("PaymentEventModel", back_populates="payment", lazy="selectin")


class PaymentEventModel(Base, BaseModel):
    __tablename__ = "payment_events"

    payment_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("payments.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    gateway_raw_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    gateway_event_id: Mapped[str | None] = mapped_column(
        String(200), nullable=True, unique=True, index=True,
    )
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)

    payment: Mapped["PaymentModel"] = relationship("PaymentModel", back_populates="events", lazy="selectin")


class GatewayConfigModel(Base, BaseModel):
    __tablename__ = "gateway_configs"

    gateway: Mapped[str] = mapped_column(String(30), default="mercado_pago")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    api_key_encrypted: Mapped[str] = mapped_column(Text, default="")
    webhook_secret_encrypted: Mapped[str] = mapped_column(Text, default="")
    public_key: Mapped[str] = mapped_column(Text, default="")
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)

    __table_args__ = (UniqueConstraint("tenant_id", "gateway", name="uq_gw_tenant_gateway"),)


class SubscriptionPaymentModel(Base, BaseModel):
    __tablename__ = "subscription_payments"

    subscription_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    payment_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("payments.id", ondelete="RESTRICT"), nullable=False, unique=True,
    )
    amount: Mapped[int] = mapped_column(Integer, default=0)
    billing_period_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    billing_period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    attempt_number: Mapped[int] = mapped_column(Integer, default=1)
