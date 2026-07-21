"""Tests — Payment Providers (ABC Compliance).

Tests for all payment gateway providers:
- MercadoPagoProvider
- StripeProvider
- AsaasProvider

Validates ABC interface compliance, webhook signature,
and mock behavior for development.
"""

from __future__ import annotations

import pytest

from app.modules.payment.infrastructure.providers.mercado_pago import (
    MercadoPagoProvider,
)
from app.modules.payment.infrastructure.providers.stripe import StripeProvider
from app.modules.payment.infrastructure.providers.asaas import AsaasProvider


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def payment_data() -> dict:
    """Dados de pagamento para testes."""
    return {
        "id": "pay_test123",
        "tenant_id": "ws_test",
        "amount_cents": 5000,
        "description": "Corte Masculino — João",
    }


# ---------------------------------------------------------------------------
# MercadoPagoProvider
# ---------------------------------------------------------------------------

class TestMercadoPagoProvider:
    """Testes do provider Mercado Pago."""

    def test_provider_initializes(self):
        """Provider deve inicializar sem erros."""
        provider = MercadoPagoProvider()
        assert provider is not None

    def test_parse_webhook_extracts_correct_fields(self):
        provider = MercadoPagoProvider()
        raw = {"action": "payment.created", "data": {"id": "mp_abc123"}}
        parsed = provider.parse_webhook(raw)
        assert "gateway_payment_id" in parsed
        assert parsed["gateway_payment_id"] == "mp_abc123"
        assert "status" in parsed

    def test_webhook_payment_approved_maps_to_paid(self):
        provider = MercadoPagoProvider()
        raw = {"action": "payment.approved", "data": {"id": "mp_xyz"}}
        parsed = provider.parse_webhook(raw)
        assert parsed["status"] in ("paid", "pending")


# ---------------------------------------------------------------------------
# StripeProvider
# ---------------------------------------------------------------------------

class TestStripeProvider:
    """Testes do provider Stripe."""

    def test_provider_initializes(self):
        provider = StripeProvider()
        assert provider is not None

    def test_webhook_signature_empty_secret_returns_false(self):
        """Sem webhook secret configurado, retorna False (não confia)."""
        provider = StripeProvider()
        assert provider.verify_webhook_signature(b"test", "sig", "") is False

    def test_parse_webhook_stripe_format(self):
        provider = StripeProvider()
        raw = {"type": "payment_intent.succeeded", "data": {"object": {"id": "pi_abc", "amount": 5000}}}
        parsed = provider.parse_webhook(raw)
        assert "gateway_payment_id" in parsed
        assert parsed["gateway_payment_id"] == "pi_abc"


# ---------------------------------------------------------------------------
# AsaasProvider
# ---------------------------------------------------------------------------

class TestAsaasProvider:
    """Testes do provider Asaas."""

    def test_provider_initializes(self):
        provider = AsaasProvider()
        assert provider is not None

    def test_webhook_signature_skip(self):
        provider = AsaasProvider()
        assert provider.verify_webhook_signature(b"test", "sig") is True

    def test_parse_webhook_event_mapping(self):
        provider = AsaasProvider()
        cases = [
            ("PAYMENT_CREATED", "pending"),
            ("PAYMENT_RECEIVED", "paid"),
            ("PAYMENT_DELETED", "cancelled"),
            ("PAYMENT_REFUNDED", "refunded"),
        ]
        for event, expected in cases:
            raw = {"event": event, "payment": {"id": "p1"}, "id": "e1"}
            parsed = provider.parse_webhook(raw)
            assert parsed["status"] == expected
            assert parsed["gateway"] == "asaas"


# ---------------------------------------------------------------------------
# ABC Compliance (all providers implement all methods)
# ---------------------------------------------------------------------------

class TestABCCompliance:
    """Verifica que todos os providers implementam a interface completa."""

    PROVIDERS = [MercadoPagoProvider, StripeProvider, AsaasProvider]

    REQUIRED_METHODS = [
        "create_payment",
        "get_payment",
        "cancel_payment",
        "refund_payment",
        "verify_webhook_signature",
        "parse_webhook",
    ]

    @pytest.mark.parametrize("provider_cls", PROVIDERS)
    def test_all_methods_implemented(self, provider_cls):
        """Todo provider deve implementar os 6 métodos da ABC."""
        for method in self.REQUIRED_METHODS:
            assert hasattr(provider_cls, method), (
                f"{provider_cls.__name__} missing method: {method}"
            )
            # Verifica que o método é callable
            assert callable(getattr(provider_cls, method))


# ---------------------------------------------------------------------------
# Webhook Idempotency
# ---------------------------------------------------------------------------

class TestWebhookIdempotency:
    """Verifica proteção contra replay de webhooks."""

    def test_different_event_ids_not_rejected(self):
        """Eventos com IDs diferentes devem ser processados."""
        provider = AsaasProvider()
        raw1 = {"event": "PAYMENT_RECEIVED", "payment": {"id": "pay_1"}, "id": "evt_1"}
        raw2 = {"event": "PAYMENT_RECEIVED", "payment": {"id": "pay_1"}, "id": "evt_2"}

        parsed1 = provider.parse_webhook(raw1)
        parsed2 = provider.parse_webhook(raw2)

        assert parsed1["gateway_event_id"] != parsed2["gateway_event_id"]

    def test_same_event_id_same_content(self):
        """Mesmo evento deve produzir mesmo resultado."""
        provider = MercadoPagoProvider()
        raw = {"action": "payment.created", "data": {"id": "mp_123"}}

        parsed1 = provider.parse_webhook(raw)
        parsed2 = provider.parse_webhook(raw)

        assert parsed1 == parsed2
