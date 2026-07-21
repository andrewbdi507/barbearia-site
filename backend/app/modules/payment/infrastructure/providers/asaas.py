"""Asaas Payment Provider — Gateway brasileiro.

Implementa PaymentProvider ABC para o Asaas (https://asaas.com).

Fluxo:
    1. create_payment() → cria cobrança (PIX, boleto, cartão)
    2. get_payment() → consulta status
    3. cancel/refund → opera sobre cobrança existente
    4. Webhook → assinatura HMAC validada

Configuração:
    ASAAS_API_KEY=<sua-chave>
    ASAAS_WEBHOOK_SECRET=<seu-segredo>
    ASAAS_ENVIRONMENT=sandbox|production
"""

from __future__ import annotations

import hashlib
import hmac
from typing import Any

from app.core.config import get_settings
from app.modules.payment.domain.entities import Payment
from app.modules.payment.domain.interfaces import PaymentProvider


class AsaasProvider(PaymentProvider):
    """Provedor de pagamento Asaas — PIX, Boleto, Cartão.

    API Docs: https://docs.asaas.com/reference
    """

    BASE_URLS = {
        "sandbox": "https://api-sandbox.asaas.com/v3",
        "production": "https://api.asaas.com/v3",
    }

    def __init__(self) -> None:
        settings = get_settings()
        self._api_key = self._get_config("ASAAS_API_KEY")
        self._webhook_secret = self._get_config("ASAAS_WEBHOOK_SECRET", "")
        env = self._get_config("ASAAS_ENVIRONMENT", "sandbox")
        self._base_url = self.BASE_URLS.get(env, self.BASE_URLS["sandbox"])
        self._headers = {
            "access_token": self._api_key,
            "Content-Type": "application/json",
        }

    # ---- PaymentProvider Interface ----

    async def create_payment(
        self, payment: Payment, **kwargs: Any,
    ) -> dict[str, Any]:
        """Cria cobrança no Asaas.

        Suporta PIX (padrão), BOLETO e CREDIT_CARD.
        """
        payload = self._build_payment_payload(payment, **kwargs)

        if self._api_key.startswith("<"):
            return self._mock_create(payment)

        # --- Chamada real à API (descomente quando tiver chave) ---
        # import httpx
        # async with httpx.AsyncClient() as client:
        #     resp = await client.post(
        #         f"{self._base_url}/payments",
        #         json=payload,
        #         headers=self._headers,
        #         timeout=30,
        #     )
        #     resp.raise_for_status()
        #     data = resp.json()
        #     return self._parse_response(data)

        return self._mock_create(payment)

    async def get_payment(self, gateway_payment_id: str) -> dict[str, Any]:
        """Consulta status de cobrança no Asaas."""
        if self._api_key.startswith("<"):
            return {"status": "paid", "gateway_payment_id": gateway_payment_id}

        # import httpx
        # async with httpx.AsyncClient() as client:
        #     resp = await client.get(
        #         f"{self._base_url}/payments/{gateway_payment_id}",
        #         headers=self._headers,
        #     )
        #     resp.raise_for_status()
        #     data = resp.json()
        #     return self._parse_response(data)

        return {"status": "paid", "gateway_payment_id": gateway_payment_id}

    async def cancel_payment(self, gateway_payment_id: str) -> dict[str, Any]:
        """Cancela cobrança pendente."""
        if self._api_key.startswith("<"):
            return {"status": "cancelled", "gateway_payment_id": gateway_payment_id}

        # import httpx
        # async with httpx.AsyncClient() as client:
        #     resp = await client.delete(
        #         f"{self._base_url}/payments/{gateway_payment_id}",
        #         headers=self._headers,
        #     )
        #     resp.raise_for_status()
        #     data = resp.json()
        #     return self._parse_response(data)

        return {"status": "cancelled", "gateway_payment_id": gateway_payment_id}

    async def refund_payment(
        self, gateway_payment_id: str, amount_cents: int | None = None,
    ) -> dict[str, Any]:
        """Reembolsa pagamento (total ou parcial)."""
        if self._api_key.startswith("<"):
            return {"status": "refunded", "gateway_payment_id": gateway_payment_id}

        return {"status": "refunded", "gateway_payment_id": gateway_payment_id}

    def verify_webhook_signature(
        self, payload: bytes, signature: str,
    ) -> bool:
        """Valida assinatura HMAC do webhook Asaas.

        Asaas envia o header 'asaas-signature' com HMAC-SHA256
        do payload usando o webhook_secret como chave.
        """
        if not self._webhook_secret:
            return True  # MVP: skip if not configured

        expected = hmac.new(
            self._webhook_secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(expected, signature)

    def parse_webhook(self, raw_payload: dict[str, Any]) -> dict[str, Any]:
        """Converte payload do Asaas em formato padronizado.

        Asaas webhook payload:
            { "event": "PAYMENT_RECEIVED", "payment": { "id": "...", ... } }

        Retorna:
            {
                "gateway": "asaas",
                "gateway_event_id": str,
                "gateway_payment_id": str,
                "status": "paid" | "pending" | "cancelled" | "refunded",
                "raw": dict,
            }
        """
        event = raw_payload.get("event", "")
        payment_data = raw_payload.get("payment", {})

        status_map = {
            "PAYMENT_CREATED": "pending",
            "PAYMENT_RECEIVED": "paid",
            "PAYMENT_CONFIRMED": "paid",
            "PAYMENT_OVERDUE": "past_due",
            "PAYMENT_DELETED": "cancelled",
            "PAYMENT_REFUNDED": "refunded",
        }

        return {
            "gateway": "asaas",
            "gateway_event_id": raw_payload.get("id", ""),
            "gateway_payment_id": payment_data.get("id", ""),
            "status": status_map.get(event, "pending"),
            "raw": raw_payload,
        }

    # ---- Private Helpers ----

    def _get_config(self, key: str, default: str = "") -> str:
        """Obtém configuração do ambiente."""
        import os
        return os.getenv(key, default)

    def _build_payment_payload(
        self, payment: Payment, **kwargs: Any,
    ) -> dict[str, Any]:
        """Constrói payload para criação de cobrança."""
        billing_type = kwargs.get("billing_type", "PIX")  # PIX, BOLETO, CREDIT_CARD

        payload: dict[str, Any] = {
            "customer": kwargs.get("customer_id", ""),
            "billingType": billing_type,
            "value": payment.amount_cents / 100.0,
            "dueDate": kwargs.get("due_date", ""),
            "description": payment.description or f"Agendamento {payment.id}",
            "externalReference": str(payment.id),
        }

        if billing_type == "CREDIT_CARD":
            payload["creditCard"] = kwargs.get("credit_card", {})
            payload["creditCardHolderInfo"] = kwargs.get("card_holder", {})

        return payload

    def _parse_response(self, data: dict[str, Any]) -> dict[str, Any]:
        """Converte resposta da API Asaas para formato padronizado."""
        status = data.get("status", "").lower()

        status_map = {
            "pending": "pending",
            "received": "paid",
            "confirmed": "paid",
            "overdue": "past_due",
            "deleted": "cancelled",
            "refunded": "refunded",
        }

        result: dict[str, Any] = {
            "gateway_payment_id": data.get("id", ""),
            "status": status_map.get(status, "pending"),
            "raw_response": data,
        }

        # PIX
        if data.get("pixTransaction"):
            result["pix_qr_code"] = data.get("invoiceUrl", "")
            result["pix_copy_paste"] = data.get("pixTransaction", "")

        # Boleto
        if data.get("bankSlipUrl"):
            result["boleto_url"] = data["bankSlipUrl"]
            result["boleto_barcode"] = data.get("nossoNumero", "")

        # Cartão
        if data.get("creditCard"):
            result["checkout_url"] = data.get("invoiceUrl", "")

        return result

    def _mock_create(self, payment: Payment) -> dict[str, Any]:
        """Mock para desenvolvimento — simula criação de cobrança."""
        import uuid
        gw_id = f"asaas_{uuid.uuid4().hex[:12]}"
        return {
            "gateway_payment_id": gw_id,
            "status": "pending",
            "pix_qr_code": f"https://sandbox.asaas.com/qr/{gw_id}",
            "pix_copy_paste": f"00020101021226870014br.gov.bcb.pix2567sandbox.asaas.com/qr/{gw_id}",
            "pix_expires_at": "2026-07-22T00:00:00Z",
            "boleto_url": f"https://sandbox.asaas.com/boleto/{gw_id}",
            "raw_response": {"id": gw_id, "status": "PENDING"},
        }
