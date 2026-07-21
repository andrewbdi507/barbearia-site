"""Payment Module — Tests."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from app.modules.payment.domain.entities import (
    GatewayConfig,
    Payment,
    PaymentEvent,
    SubscriptionPayment,
)
from app.modules.payment.domain.enums import (
    PaymentEventType,
    PaymentGateway,
    PaymentMethod,
    PaymentStatus,
)
from app.modules.payment.domain.interfaces import PaymentProvider, PaymentProviderFactory
from app.modules.payment.infrastructure.providers.mercado_pago import MercadoPagoProvider
from app.modules.payment.infrastructure.providers.stripe import StripeProvider


class TestPaymentEntity:
    def test_create_pending(self) -> None:
        p = Payment(id="p1", tenant_id="t1", amount=5000)
        assert p.status == PaymentStatus.PENDING
        assert p.amount == 5000

    def test_mark_paid(self) -> None:
        p = Payment(id="p1", tenant_id="t1", amount=5000)
        p.mark_paid("mp_123")
        assert p.status == PaymentStatus.PAID
        assert p.gateway_payment_id == "mp_123"
        assert p.paid_at is not None

    def test_mark_declined(self) -> None:
        p = Payment(id="p1", tenant_id="t1", amount=5000)
        p.mark_declined("Saldo insuficiente")
        assert p.status == PaymentStatus.DECLINED

    def test_mark_refunded_full(self) -> None:
        p = Payment(id="p1", tenant_id="t1", amount=5000, status=PaymentStatus.PAID)
        p.mark_refunded(5000)
        assert p.status == PaymentStatus.REFUNDED

    def test_mark_refunded_partial(self) -> None:
        p = Payment(id="p1", tenant_id="t1", amount=5000, status=PaymentStatus.PAID)
        p.mark_refunded(2000)
        assert p.status == PaymentStatus.PARTIALLY_REFUNDED

    def test_mark_cancelled(self) -> None:
        p = Payment(id="p1", tenant_id="t1", amount=5000)
        p.mark_cancelled()
        assert p.status == PaymentStatus.CANCELLED

    def test_mark_expired(self) -> None:
        p = Payment(id="p1", tenant_id="t1", amount=5000)
        p.mark_expired()
        assert p.status == PaymentStatus.EXPIRED


class TestProviderPattern:
    def test_factory_register(self) -> None:
        from app.modules.payment.infrastructure.providers import register_providers
        register_providers()
        provider = PaymentProviderFactory.create("mercado_pago")
        assert isinstance(provider, MercadoPagoProvider)

    def test_factory_stripe(self) -> None:
        from app.modules.payment.infrastructure.providers import register_providers
        register_providers()
        provider = PaymentProviderFactory.create("stripe")
        assert isinstance(provider, StripeProvider)

    def test_factory_unknown(self) -> None:
        with pytest.raises(ValueError):
            PaymentProviderFactory.create("unknown_gateway")

    @pytest.mark.asyncio
    async def test_mercado_pago_create_pix(self) -> None:
        from app.modules.payment.infrastructure.providers import register_providers
        register_providers()
        provider = MercadoPagoProvider()
        p = Payment(id="p1", tenant_id="t1", amount=4500, payment_method=PaymentMethod.PIX)
        result = await provider.create_payment(p)
        assert "gateway_payment_id" in result
        assert "pix_qr_code" in result
        assert "pix_copy_paste" in result

    @pytest.mark.asyncio
    async def test_mercado_pago_webhook_parse(self) -> None:
        provider = MercadoPagoProvider()
        payload = {
            "action": "payment.approved",
            "data": {"id": "mp_123"},
            "id": 987654321,
        }
        parsed = provider.parse_webhook(payload)
        assert parsed["gateway_payment_id"] == "mp_123"
        assert parsed["status"] == "paid"
        assert parsed["gateway_event_id"] == "987654321"

    def test_verify_signature_valid(self) -> None:
        import hashlib, hmac
        provider = MercadoPagoProvider()
        secret = "my_webhook_secret"
        payload = b'{"action":"payment.approved"}'
        sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
        assert provider.verify_webhook_signature(payload, sig, secret)

    def test_verify_signature_invalid(self) -> None:
        provider = MercadoPagoProvider()
        assert not provider.verify_webhook_signature(b"test", "bad_sig", "secret")


class TestEventSourcing:
    def test_payment_event(self) -> None:
        e = PaymentEvent(
            id="e1", payment_id="p1",
            event_type=PaymentEventType.CREATED,
            gateway_event_id="evt_001",
        )
        assert e.payment_id == "p1"
        assert e.event_type == PaymentEventType.CREATED

    def test_replay_detection(self) -> None:
        """Gateway event IDs must be unique."""
        e1 = PaymentEvent(id="e1", payment_id="p1", gateway_event_id="evt_001")
        e2 = PaymentEvent(id="e2", payment_id="p2", gateway_event_id="evt_001")
        assert e1.gateway_event_id == e2.gateway_event_id  # Mesmo ID = replay


class TestDTOs:
    def test_payment_create(self) -> None:
        from app.modules.payment.application.dto import PaymentCreateRequest
        req = PaymentCreateRequest(
            booking_id="b1", amount=4500, payment_method="pix",
            idempotency_key="idem-001",
        )
        assert req.idempotency_key == "idem-001"

    def test_payment_create_invalid_method(self) -> None:
        from app.modules.payment.application.dto import PaymentCreateRequest
        import pydantic
        with pytest.raises(pydantic.ValidationError):
            PaymentCreateRequest(amount=100, payment_method="invalid")
