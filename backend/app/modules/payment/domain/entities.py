"""Payment Module — Domain Entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.modules.payment.domain.enums import (
    PaymentEventType,
    PaymentGateway,
    PaymentMethod,
    PaymentStatus,
)


@dataclass
class Payment:
    """Aggregate Root — Pagamento.

    NUNCA armazena dados de cartão (PCI-DSS).
    Apenas referencia o gateway_payment_id.
    """

    id: str
    tenant_id: str
    booking_id: str | None = None  # Opcional: pagamento de assinatura
    subscription_id: str | None = None
    customer_id: str | None = None
    amount: int = 0  # centavos
    original_amount: int = 0  # antes de desconto/estorno
    currency: str = "BRL"
    status: PaymentStatus = PaymentStatus.PENDING
    payment_method: PaymentMethod | None = None
    gateway: PaymentGateway = PaymentGateway.MERCADO_PAGO
    gateway_payment_id: str | None = None
    gateway_checkout_url: str | None = None
    pix_qr_code: str | None = None
    pix_copy_paste: str | None = None
    pix_expires_at: datetime | None = None
    idempotency_key: str | None = None
    deposit_type: str = "none"
    deposit_value: int = 0
    paid_at: datetime | None = None
    refunded_at: datetime | None = None
    refunded_amount: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def mark_paid(self, gateway_payment_id: str) -> None:
        self.status = PaymentStatus.PAID
        self.gateway_payment_id = gateway_payment_id
        self.paid_at = datetime.now(timezone.utc)

    def mark_declined(self, reason: str = "") -> None:
        self.status = PaymentStatus.DECLINED
        self.metadata["decline_reason"] = reason

    def mark_refunded(self, amount: int) -> None:
        self.refunded_amount = amount
        self.status = PaymentStatus.REFUNDED if amount >= self.amount else PaymentStatus.PARTIALLY_REFUNDED
        self.refunded_at = datetime.now(timezone.utc)

    def mark_cancelled(self) -> None:
        self.status = PaymentStatus.CANCELLED

    def mark_expired(self) -> None:
        self.status = PaymentStatus.EXPIRED


@dataclass
class PaymentEvent:
    """Event sourcing — registro imutável de cada mudança de estado (append-only)."""

    id: str
    payment_id: str
    event_type: PaymentEventType = PaymentEventType.CREATED
    gateway_raw_data: dict[str, Any] = field(default_factory=dict)
    gateway_event_id: str | None = None  # Previne replay
    ip_address: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class GatewayConfig:
    """Configuração criptografada do gateway por tenant."""

    id: str
    tenant_id: str
    gateway: PaymentGateway = PaymentGateway.MERCADO_PAGO
    is_active: bool = True
    api_key_encrypted: str = ""  # AES-256-GCM
    webhook_secret_encrypted: str = ""
    public_key: str = ""
    settings: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class SubscriptionPayment:
    """Pagamento de assinatura SaaS (recorrente)."""

    id: str
    tenant_id: str
    subscription_id: str
    payment_id: str
    amount: int = 0
    billing_period_start: datetime | None = None
    billing_period_end: datetime | None = None
    status: PaymentStatus = PaymentStatus.PENDING
    attempt_number: int = 1
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
