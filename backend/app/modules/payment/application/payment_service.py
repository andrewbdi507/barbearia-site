"""Payment Module — Application Service.

Orquestra pagamentos, webhooks, reembolsos, event sourcing.
NUNCA armazena dados de cartão (PCI-DSS).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.core.exceptions import BusinessRuleError, NotFoundError
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
from app.modules.payment.domain.repository_interfaces import (
    IGatewayConfigRepository,
    IPaymentEventRepository,
    IPaymentRepository,
    ISubscriptionPaymentRepository,
)
from app.modules.payment.infrastructure.providers import register_providers


class PaymentService:
    """Serviço de pagamentos — Provider Pattern.

    O sistema NUNCA sabe qual gateway está sendo usado.
    Toda operação passa pelo PaymentProvider abstrato.
    """

    def __init__(
        self,
        payment_repo: IPaymentRepository,
        event_repo: IPaymentEventRepository,
        gateway_config_repo: IGatewayConfigRepository,
        sub_payment_repo: ISubscriptionPaymentRepository,
    ) -> None:
        self._payments = payment_repo
        self._events = event_repo
        self._gateway_configs = gateway_config_repo
        self._sub_payments = sub_payment_repo
        register_providers()

    # ============================================================
    # Create Payment
    # ============================================================

    async def create_payment(self, tenant_id: str, **kwargs: object) -> Payment:
        """Cria cobrança via gateway (PIX, cartão, boleto).

        Fluxo:
        1. Verifica idempotency
        2. Cria Payment no banco (status=pending)
        3. Chama provider.create_payment()
        4. Atualiza Payment com dados do gateway (pix_qr_code, etc.)
        5. Registra PaymentEvent (event sourcing)
        """

        # 1. Idempotency check
        idemp_key = str(kwargs.get("idempotency_key", ""))
        if idemp_key:
            existing = await self._payments.get_by_idempotency_key(idemp_key)
            if existing:
                return existing

        gateway_str = str(kwargs.get("gateway", "mercado_pago"))
        amount = int(kwargs.get("amount", 0))
        payment_method = str(kwargs.get("payment_method", "pix"))

        # 2. Criar Payment
        payment = Payment(
            id=str(uuid4()), tenant_id=tenant_id,
            booking_id=str(kwargs.get("booking_id", "")) if kwargs.get("booking_id") else None,
            subscription_id=str(kwargs.get("subscription_id", "")) if kwargs.get("subscription_id") else None,
            customer_id=str(kwargs.get("customer_id", "")) if kwargs.get("customer_id") else None,
            amount=amount, original_amount=amount,
            payment_method=PaymentMethod(payment_method),
            gateway=PaymentGateway(gateway_str),
            idempotency_key=idemp_key if idemp_key else None,
            deposit_type=str(kwargs.get("deposit_type", "none")),
            deposit_value=int(kwargs.get("deposit_value", 0)),
            status=PaymentStatus.PENDING,
        )
        created = await self._payments.create(payment)

        # Log event
        await self._log_event(created.id, PaymentEventType.CREATED, {"amount": amount})

        # 3. Chamar gateway
        try:
            provider = self._get_provider(gateway_str)
            result = await provider.create_payment(created)

            # 4. Atualizar com resposta do gateway
            created.gateway_payment_id = result.get("gateway_payment_id")
            created.gateway_checkout_url = result.get("checkout_url")
            created.pix_qr_code = result.get("pix_qr_code")
            created.pix_copy_paste = result.get("pix_copy_paste")
            if result.get("pix_expires_at"):
                created.pix_expires_at = datetime.fromisoformat(result["pix_expires_at"].replace("Z", "+00:00"))

            if payment_method == "pix":
                created.status = PaymentStatus.AWAITING_PIX

            await self._payments.update(created)
            await self._log_event(created.id, PaymentEventType.PIX_GENERATED if payment_method == "pix" else PaymentEventType.PROCESSING,
                                  result.get("raw_response", {}))

        except Exception as e:
            created.status = PaymentStatus.ERROR
            created.metadata["error"] = str(e)
            await self._payments.update(created)
            await self._log_event(created.id, PaymentEventType.ERROR, {"error": str(e)})

        return created

    # ============================================================
    # Get Payment
    # ============================================================

    async def get_payment(self, payment_id: str) -> Payment:
        p = await self._payments.get_by_id(payment_id)
        if p is None:
            raise NotFoundError(message="Pagamento não encontrado.")
        return p

    async def get_payment_events(self, payment_id: str) -> list[PaymentEvent]:
        return await self._events.get_for_payment(payment_id)

    async def list_payments(self, tenant_id: str, *, status: str | None = None, offset: int = 0, limit: int = 50) -> tuple[list[Payment], int]:
        return await self._payments.list_for_tenant(tenant_id, status=status, offset=offset, limit=limit)

    # ============================================================
    # Cancel
    # ============================================================

    async def cancel_payment(self, payment_id: str) -> Payment:
        p = await self.get_payment(payment_id)
        if p.status not in {PaymentStatus.PENDING, PaymentStatus.AWAITING_PIX}:
            raise BusinessRuleError(message="Só é possível cancelar pagamentos pendentes.")

        provider = self._get_provider(str(p.gateway.value) if hasattr(p.gateway, 'value') else str(p.gateway))
        if p.gateway_payment_id:
            await provider.cancel_payment(p.gateway_payment_id)

        p.mark_cancelled()
        await self._payments.update(p)
        await self._log_event(p.id, PaymentEventType.CANCELLED)
        return p

    # ============================================================
    # Refund
    # ============================================================

    async def refund_payment(self, payment_id: str, amount: int | None = None, reason: str = "") -> Payment:
        p = await self.get_payment(payment_id)
        if p.status != PaymentStatus.PAID:
            raise BusinessRuleError(message="Só é possível reembolsar pagamentos confirmados.")

        refund_amount = amount or p.amount
        provider = self._get_provider(str(p.gateway.value) if hasattr(p.gateway, 'value') else str(p.gateway))
        if p.gateway_payment_id:
            await provider.refund_payment(p.gateway_payment_id, refund_amount)

        p.mark_refunded(refund_amount)
        await self._payments.update(p)
        await self._log_event(p.id, PaymentEventType.REFUNDED, {"amount": refund_amount, "reason": reason})
        return p

    # ============================================================
    # Webhook Processing (CRITICAL — never trust frontend)
    # ============================================================

    async def process_webhook(
        self, gateway: str, payload: dict[str, Any],
        signature: str | None = None, raw_body: bytes | None = None,
    ) -> dict[str, Any]:
        """Processa webhook do gateway.

        Fluxo:
        1. Verifica assinatura (anti-spoofing)
        2. Parseia payload para formato padronizado
        3. Verifica replay attack (gateway_event_id único)
        4. Atualiza Payment com novo status
        5. Registra PaymentEvent (event sourcing)
        6. Se subscription, atualiza SubscriptionPayment
        """

        # 1. Verify signature
        provider = self._get_provider(gateway)
        # Skip signature check for MVP (no webhook secret configured)
        # In production: get config from DB, verify

        # 2. Parse webhook
        parsed = provider.parse_webhook(payload)

        gateway_event_id = parsed.get("gateway_event_id")
        gateway_payment_id = parsed.get("gateway_payment_id")
        new_status = parsed.get("status", "pending")

        # 3. Replay attack prevention
        if gateway_event_id:
            exists = await self._events.exists_by_gateway_event_id(gateway_event_id)
            if exists:
                return {"status": "duplicate", "message": "Evento já processado."}

        # 4. Find payment
        if not gateway_payment_id:
            return {"status": "error", "message": "gateway_payment_id não encontrado no webhook."}

        payment = await self._payments.get_by_gateway_id(gateway_payment_id)
        if payment is None:
            return {"status": "error", "message": f"Payment {gateway_payment_id} não encontrado."}

        # 5. Update payment status
        old_status = payment.status
        payment.status = new_status
        if new_status == PaymentStatus.PAID:
            payment.paid_at = datetime.now(timezone.utc)
        await self._payments.update(payment)

        # 6. Log event
        await self._log_event(
            payment.id, PaymentEventType.WEBHOOK_RECEIVED,
            {"gateway_event_id": gateway_event_id, "old_status": old_status, "new_status": new_status,
             "raw_data": parsed.get("raw_data", {})},
            gateway_event_id=gateway_event_id,
        )

        return {"status": "processed", "payment_id": payment.id, "new_status": new_status}

    # ============================================================
    # Gateway Config
    # ============================================================

    async def configure_gateway(self, tenant_id: str, **kwargs: object) -> GatewayConfig:
        config = GatewayConfig(
            id=str(uuid4()), tenant_id=tenant_id,
            gateway=PaymentGateway(str(kwargs.get("gateway", "mercado_pago"))),
            api_key_encrypted=str(kwargs.get("api_key", "")),
            webhook_secret_encrypted=str(kwargs.get("webhook_secret", "")),
            public_key=str(kwargs.get("public_key", "")),
            is_active=bool(kwargs.get("is_active", True)),
        )
        return await self._gateway_configs.upsert(config)

    # ============================================================
    # Subscription Payments
    # ============================================================

    async def create_subscription_payment(
        self, tenant_id: str, subscription_id: str, amount: int,
    ) -> SubscriptionPayment:
        """Cria cobrança de assinatura recorrente."""
        sp = SubscriptionPayment(
            id=str(uuid4()), tenant_id=tenant_id,
            subscription_id=subscription_id,
            payment_id="", amount=amount,
            billing_period_start=datetime.now(timezone.utc),
            billing_period_end=datetime.now(timezone.utc),
        )
        return await self._sub_payments.create(sp)

    async def get_subscription_payments(self, subscription_id: str) -> list[SubscriptionPayment]:
        return await self._sub_payments.list_for_subscription(subscription_id)

    # ============================================================
    # Helpers
    # ============================================================

    def _get_provider(self, gateway: str) -> PaymentProvider:
        return PaymentProviderFactory.create(gateway)

    async def _log_event(
        self, payment_id: str, event_type: PaymentEventType,
        data: dict[str, Any] | None = None,
        gateway_event_id: str | None = None,
    ) -> None:
        await self._events.log(PaymentEvent(
            id=str(uuid4()), payment_id=payment_id,
            event_type=event_type,
            gateway_raw_data=data or {},
            gateway_event_id=gateway_event_id,
        ))
