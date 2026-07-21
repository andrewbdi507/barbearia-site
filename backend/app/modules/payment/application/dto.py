"""Payment Module — DTOs."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ============================================================
# Payment DTOs
# ============================================================

class PaymentCreateRequest(BaseModel):
    booking_id: str | None = None
    subscription_id: str | None = None
    amount: int = Field(..., ge=1)
    payment_method: str = Field(default="pix", pattern=r"^(pix|credit_card|boleto)$")
    gateway: str = Field(default="mercado_pago")
    idempotency_key: str | None = None
    deposit_type: str = Field(default="none")
    deposit_value: int = Field(default=0, ge=0)
    customer_id: str | None = None


class PaymentRefundRequest(BaseModel):
    amount: int | None = Field(default=None, ge=1)
    reason: str = ""


class PaymentResponse(BaseModel):
    id: str
    booking_id: str | None = None
    subscription_id: str | None = None
    amount: int
    status: str
    payment_method: str | None = None
    gateway: str
    gateway_payment_id: str | None = None
    gateway_checkout_url: str | None = None
    pix_qr_code: str | None = None
    pix_copy_paste: str | None = None
    pix_expires_at: datetime | None = None
    paid_at: datetime | None = None
    refunded_at: datetime | None = None
    refunded_amount: int
    created_at: datetime | None = None


class PaymentListResponse(BaseModel):
    items: list[PaymentResponse]
    total: int
    offset: int
    limit: int


class PaymentEventResponse(BaseModel):
    id: str
    event_type: str
    gateway_event_id: str | None = None
    created_at: datetime | None = None


# ============================================================
# Gateway Config DTOs
# ============================================================

class GatewayConfigRequest(BaseModel):
    gateway: str = "mercado_pago"
    api_key: str = ""
    webhook_secret: str = ""
    public_key: str = ""
    is_active: bool = True


# ============================================================
# Subscription Payment DTOs
# ============================================================

class SubscriptionPaymentResponse(BaseModel):
    id: str
    subscription_id: str
    amount: int
    status: str
    billing_period_start: datetime | None = None
    billing_period_end: datetime | None = None
    created_at: datetime | None = None
