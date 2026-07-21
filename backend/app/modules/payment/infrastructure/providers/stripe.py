"""Payment Module — Stripe Provider.

Implementa PaymentProvider para Stripe.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

from app.modules.payment.domain.interfaces import PaymentProvider
from app.modules.payment.domain.entities import Payment


class StripeProvider(PaymentProvider):
    """Provider para Stripe.

    Documentação: https://stripe.com/docs/api
    """

    def __init__(self, secret_key: str = "", webhook_secret: str = "") -> None:
        self._secret_key = secret_key
        self._webhook_secret = webhook_secret

    async def create_payment(self, payment: Payment, **kwargs: Any) -> dict[str, Any]:
        return {
            "gateway_payment_id": f"pi_{payment.id}",
            "status": "pending",
            "checkout_url": f"https://checkout.stripe.com/pay/{payment.id}",
            "raw_response": {"id": f"pi_{payment.id}", "status": "requires_payment_method"},
        }

    async def get_payment(self, gateway_payment_id: str) -> dict[str, Any]:
        return {"gateway_payment_id": gateway_payment_id, "status": "paid", "amount": 0, "raw_response": {}}

    async def cancel_payment(self, gateway_payment_id: str) -> dict[str, Any]:
        return {"gateway_payment_id": gateway_payment_id, "status": "cancelled", "raw_response": {}}

    async def refund_payment(self, gateway_payment_id: str, amount: int | None = None) -> dict[str, Any]:
        return {"gateway_payment_id": gateway_payment_id, "status": "refunded", "amount": amount or 0, "raw_response": {}}

    def verify_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """Stripe: stripe-signature = t=timestamp,v1=signature."""
        if not secret:
            return False
        try:
            # Simplified — production uses stripe.Webhook.construct_event()
            parts = dict(p.split("=") for p in signature.split(","))
            expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
            return hmac.compare_digest(expected, parts.get("v1", ""))
        except Exception:
            return False

    def parse_webhook(self, payload: dict[str, Any]) -> dict[str, Any]:
        event_type = payload.get("type", "unknown")
        data = payload.get("data", {}).get("object", {})
        return {
            "gateway_event_id": str(payload.get("id", "")),
            "gateway_payment_id": str(data.get("id", "")),
            "status": "paid" if event_type == "payment_intent.succeeded" else "pending",
            "amount": data.get("amount", 0),
            "raw_data": payload,
        }
