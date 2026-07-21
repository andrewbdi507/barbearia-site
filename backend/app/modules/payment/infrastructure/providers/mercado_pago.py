"""Payment Module — MercadoPago Provider.

Implementa PaymentProvider para Mercado Pago.
Suporta: PIX, Cartão de Crédito, Boleto.

PCI-DSS: Nunca armazena dados de cartão.
Todo processamento via SDK/API do Mercado Pago.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

from app.modules.payment.domain.interfaces import PaymentProvider
from app.modules.payment.domain.entities import Payment


class MercadoPagoProvider(PaymentProvider):
    """Provider para Mercado Pago.

    Documentação: https://www.mercadopago.com.br/developers/pt/reference
    """

    def __init__(self, access_token: str = "", public_key: str = "") -> None:
        self._access_token = access_token
        self._public_key = public_key
        self._base_url = "https://api.mercadopago.com/v1"

    # ============================================================
    # Create Payment
    # ============================================================

    async def create_payment(self, payment: Payment, **kwargs: Any) -> dict[str, Any]:
        """Cria cobrança no Mercado Pago.

        No MVP, simula a criação retornando dados mockados.
        Em produção: POST /v1/payments com SDK do Mercado Pago.
        """
        payment_method = payment.payment_method.value if payment.payment_method else "pix"

        result: dict[str, Any] = {
            "gateway_payment_id": f"mp_{payment.id}",
            "status": "pending",
            "raw_response": {"id": f"mp_{payment.id}", "status": "pending"},
        }

        if payment_method == "pix":
            result.update({
                "pix_qr_code": f"00020101021226860014br.gov.bcb.pix2567mp_{payment.id}",
                "pix_copy_paste": f"00020101021226860014br.gov.bcb.pix2567mp_{payment.id}5204000053039865405{payment.amount / 100:.2f}",
                "pix_expires_at": "2026-07-21T23:59:59Z",
            })

        # TODO: Integrar com SDK real do MercadoPago
        # import mercadopago
        # sdk = mercadopago.SDK(self._access_token)
        # payment_data = {
        #     "transaction_amount": payment.amount / 100,
        #     "payment_method_id": payment_method,
        #     "payer": {"email": kwargs.get("payer_email")},
        #     ...
        # }
        # result = sdk.payment().create(payment_data)

        return result

    # ============================================================
    # Get / Cancel / Refund
    # ============================================================

    async def get_payment(self, gateway_payment_id: str) -> dict[str, Any]:
        """Consulta status no Mercado Pago."""
        return {
            "gateway_payment_id": gateway_payment_id,
            "status": "paid",
            "amount": 0,
            "raw_response": {"id": gateway_payment_id, "status": "approved"},
        }

    async def cancel_payment(self, gateway_payment_id: str) -> dict[str, Any]:
        return {
            "gateway_payment_id": gateway_payment_id,
            "status": "cancelled",
            "raw_response": {"id": gateway_payment_id, "status": "cancelled"},
        }

    async def refund_payment(self, gateway_payment_id: str, amount: int | None = None) -> dict[str, Any]:
        return {
            "gateway_payment_id": gateway_payment_id,
            "status": "refunded",
            "amount": amount or 0,
            "raw_response": {"id": gateway_payment_id, "status": "refunded"},
        }

    # ============================================================
    # Webhook
    # ============================================================

    def verify_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """Verifica assinatura x-signature do Mercado Pago.

        Mercado Pago envia:
        - x-signature: HMAC-SHA256 do payload com webhook_secret
        - x-request-id: ID único da notificação (anti-replay)
        """
        if not secret:
            return False
        expected = hmac.new(
            secret.encode(), payload, hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def parse_webhook(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Converte webhook do Mercado Pago para formato padronizado.

        Payload esperado:
        {
            "action": "payment.updated",
            "data": {"id": "mp_123"},
            "date_created": "...",
            "id": 123456789
        }
        """
        action = payload.get("action", "unknown")
        data = payload.get("data", {})

        return {
            "gateway_event_id": str(payload.get("id", "")),
            "gateway_payment_id": str(data.get("id", "")),
            "status": self._map_status(action),
            "amount": 0,  # MercadoPago webhook não inclui amount; precisa GET /v1/payments/:id
            "raw_data": payload,
        }

    @staticmethod
    def _map_status(action: str) -> str:
        mapping = {
            "payment.created": "processing",
            "payment.updated": "processing",
            "payment.approved": "paid",
            "payment.rejected": "declined",
            "payment.cancelled": "cancelled",
            "payment.refunded": "refunded",
        }
        return mapping.get(action, "pending")
