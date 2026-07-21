"""Payment Module — Domain Enums."""

from __future__ import annotations

from enum import StrEnum


class PaymentStatus(StrEnum):
    PENDING = "pending"
    AWAITING_PIX = "awaiting_pix"
    PROCESSING = "processing"
    PAID = "paid"
    DECLINED = "declined"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    EXPIRED = "expired"
    ERROR = "error"


class PaymentMethod(StrEnum):
    PIX = "pix"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BOLETO = "boleto"


class PaymentGateway(StrEnum):
    MERCADO_PAGO = "mercado_pago"
    STRIPE = "stripe"
    ASAAS = "asaas"
    PAGSEGURO = "pagseguro"
    STONE = "stone"


class PaymentEventType(StrEnum):
    CREATED = "payment.created"
    PIX_GENERATED = "payment.pix_generated"
    PROCESSING = "payment.processing"
    APPROVED = "payment.approved"
    DECLINED = "payment.declined"
    CANCELLED = "payment.cancelled"
    REFUNDED = "payment.refunded"
    EXPIRED = "payment.expired"
    ERROR = "payment.error"
    WEBHOOK_RECEIVED = "webhook.received"


class SubscriptionEventType(StrEnum):
    CREATED = "subscription.created"
    RENEWED = "subscription.renewed"
    CANCELLED = "subscription.cancelled"
    SUSPENDED = "subscription.suspended"
    UPGRADED = "subscription.upgraded"
    DOWNGRADED = "subscription.downgraded"
    PAYMENT_FAILED = "subscription.payment_failed"


class DepositType(StrEnum):
    NONE = "none"
    FIXED = "fixed"
    PERCENTAGE = "percentage"
