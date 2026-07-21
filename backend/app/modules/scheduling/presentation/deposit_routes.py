"""Payment + Booking integration — Deposit flow.

Conecta o módulo de pagamento ao módulo de agendamento.
Quando um booking exige depósito, cria um pagamento e aguarda
confirmação via webhook antes de confirmar o agendamento.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.payment.domain.entities import Payment
from app.modules.payment.domain.enums import PaymentGateway, PaymentMethod, PaymentStatus
from app.modules.payment.domain.interfaces import PaymentProviderFactory
from app.modules.tenant.presentation.dependencies import get_current_tenant
from app.core.config import get_settings

deposit_router = APIRouter(prefix="/bookings", tags=["Booking Payments"])


async def create_deposit_payment(
    booking_id: str,
    tenant_id: str,
    service_name: str,
    amount_cents: int,
    deposit_pct: int = 20,
    payment_method: str = "pix",
) -> dict[str, Any]:
    """Cria pagamento de depósito/sinal para um agendamento.

    Args:
        booking_id: ID do agendamento
        tenant_id: ID do tenant
        service_name: Nome do serviço (descrição)
        amount_cents: Valor total em centavos
        deposit_pct: Percentual do sinal (padrão 20%)
        payment_method: Método (pix, credit_card, boleto)

    Returns:
        Dict com payment info (id, checkout_url, pix_qr_code, etc.)
    """
    deposit_amount = int(amount_cents * deposit_pct / 100)

    payment = Payment(
        id=str(uuid4()),
        tenant_id=tenant_id,
        booking_id=booking_id,
        amount=deposit_amount,
        original_amount=amount_cents,
        currency="BRL",
        status=PaymentStatus.PENDING,
        payment_method=PaymentMethod(payment_method),
        gateway=PaymentGateway.MERCADO_PAGO,
        idempotency_key=f"booking_{booking_id}",
        deposit_type="percent",
        deposit_value=deposit_pct,
        metadata={
            "booking_id": booking_id,
            "service_name": service_name,
            "deposit_pct": deposit_pct,
        },
    )

    provider = PaymentProviderFactory.create(PaymentGateway.MERCADO_PAGO)
    result = await provider.create_payment(
        payment,
        description=f"Sinal ({deposit_pct}%) — {service_name}",
    )

    payment.gateway_payment_id = result.get("gateway_payment_id")
    payment.gateway_checkout_url = result.get("checkout_url")
    payment.pix_qr_code = result.get("pix_qr_code")
    payment.pix_copy_paste = result.get("pix_copy_paste")
    payment.pix_expires_at = result.get("pix_expires_at")

    return {
        "payment_id": payment.id,
        "gateway_payment_id": payment.gateway_payment_id,
        "amount": deposit_amount,
        "currency": "BRL",
        "checkout_url": payment.gateway_checkout_url,
        "pix_qr_code": payment.pix_qr_code,
        "pix_copy_paste": payment.pix_copy_paste,
        "expires_in_minutes": 15,
    }


def get_effective_deposit_pct(tenant_settings: dict | None = None) -> int:
    """Calcula percentual de depósito baseado nas configs do tenant.

    Prioridade: tenant_settings > default (20%)
    """
    if tenant_settings:
        require = tenant_settings.get("require_payment", False)
        if not require:
            return 0
        return tenant_settings.get("deposit_value", 20)
    return 20  # default


@deposit_router.post("/{booking_id}/pay-deposit")
async def pay_booking_deposit(
    booking_id: str,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, Any]:
    """Inicia pagamento do sinal para confirmar o agendamento.

    Retorna dados do pagamento (PIX ou checkout URL).
    O booking é confirmado automaticamente quando o webhook
    do gateway notificar o pagamento aprovado.
    """
    from app.modules.scheduling.infrastructure.repository import BookingRepository
    from app.modules.payment.infrastructure.repository import PaymentRepository

    booking_repo = BookingRepository(session)
    booking = await booking_repo.get_by_id(booking_id)

    if booking is None:
        return {"error": "Booking not found"}, 404

    # Get service price
    service_price = getattr(booking, 'total_amount', 5000)  # fallback R$50
    service_name = getattr(booking, 'service_name', 'Serviço')

    # Check if deposit already paid
    payment_repo = PaymentRepository(session)
    existing = await payment_repo.get_by_booking_id(booking_id)
    if existing and existing.get("status") == "paid":
        return {"status": "already_paid", "message": "Pagamento já confirmado"}

    deposit_pct = 20  # default, TODO: read from tenant settings
    result = await create_deposit_payment(
        booking_id=booking_id,
        tenant_id=tenant["id"],
        service_name=service_name,
        amount_cents=service_price,
        deposit_pct=deposit_pct,
    )

    # Save payment to DB
    await payment_repo.create(result)

    # Mark booking as waiting payment
    await booking_repo.update_status(booking_id, "waiting_payment")

    return {
        "status": "pending_payment",
        "deposit_percent": deposit_pct,
        "expires_in_minutes": 15,
        **result,
    }
