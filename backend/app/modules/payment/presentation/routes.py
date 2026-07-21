"""Payment Module — API Routes + Webhooks."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.payment.application.dto import (
    GatewayConfigRequest,
    PaymentCreateRequest,
    PaymentEventResponse,
    PaymentListResponse,
    PaymentRefundRequest,
    PaymentResponse,
    SubscriptionPaymentResponse,
)
from app.modules.payment.application.payment_service import PaymentService
from app.modules.payment.infrastructure.repository import (
    GatewayConfigRepository,
    PaymentEventRepository,
    PaymentRepository,
    SubscriptionPaymentRepository,
)
from app.modules.tenant.presentation.dependencies import get_current_tenant

router = APIRouter(prefix="/payments", tags=["Payments"])
webhook_router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


def _get_service(session: AsyncSession) -> PaymentService:
    return PaymentService(
        payment_repo=PaymentRepository(session),
        event_repo=PaymentEventRepository(session),
        gateway_config_repo=GatewayConfigRepository(session),
        sub_payment_repo=SubscriptionPaymentRepository(session),
    )


# ============================================================
# PAYMENTS
# ============================================================

@router.post("", response_model=PaymentResponse, status_code=201)
async def create_payment(
    body: PaymentCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> PaymentResponse:
    svc = _get_service(session)
    p = await svc.create_payment(tenant["id"], **body.model_dump())
    return _payment_response(p)


@router.get("", response_model=PaymentListResponse)
async def list_payments(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    status: str | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> PaymentListResponse:
    svc = _get_service(session)
    items, total = await svc.list_payments(tenant["id"], status=status, offset=offset, limit=limit)
    return PaymentListResponse(
        items=[_payment_response(p) for p in items],
        total=total, offset=offset, limit=limit,
    )


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> PaymentResponse:
    svc = _get_service(session)
    p = await svc.get_payment(payment_id)
    return _payment_response(p)


@router.get("/{payment_id}/events", response_model=list[PaymentEventResponse])
async def get_payment_events(
    payment_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[PaymentEventResponse]:
    svc = _get_service(session)
    events = await svc.get_payment_events(payment_id)
    return [PaymentEventResponse(**e.__dict__) for e in events]


@router.post("/{payment_id}/cancel", response_model=PaymentResponse)
async def cancel_payment(
    payment_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> PaymentResponse:
    svc = _get_service(session)
    p = await svc.cancel_payment(payment_id)
    return _payment_response(p)


@router.post("/{payment_id}/refund", response_model=PaymentResponse)
async def refund_payment(
    payment_id: str,
    body: PaymentRefundRequest,
    session: AsyncSession = Depends(get_async_session),
) -> PaymentResponse:
    svc = _get_service(session)
    p = await svc.refund_payment(payment_id, body.amount, body.reason)
    return _payment_response(p)


# ============================================================
# GATEWAY CONFIG
# ============================================================

@router.post("/gateway/config")
async def configure_gateway(
    body: GatewayConfigRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.configure_gateway(tenant["id"], **body.model_dump())
    return {"message": "Gateway configurado."}


# ============================================================
# SUBSCRIPTION PAYMENTS
# ============================================================

@router.get("/subscriptions/{subscription_id}", response_model=list[SubscriptionPaymentResponse])
async def get_subscription_payments(
    subscription_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[SubscriptionPaymentResponse]:
    svc = _get_service(session)
    items = await svc.get_subscription_payments(subscription_id)
    return [SubscriptionPaymentResponse(**sp.__dict__) for sp in items]


# ============================================================
# WEBHOOK (PUBLIC — não requer auth)
# ============================================================

@webhook_router.post("/mercado-pago")
@webhook_router.post("/stripe")
@webhook_router.post("/{gateway}")
async def receive_webhook(
    request: Request,
    gateway: str = "",
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Endpoint público de webhook.

    Processa notificações de TODOS os gateways.
    Valida assinatura antes de processar.
    Responde 200 imediatamente (processamento assíncrono).
    """
    if session is None:
        return {"status": "error", "message": "Session not available"}

    # Resolver gateway da URL se não especificado
    if not gateway or gateway == "{gateway}":
        path = request.url.path
        if "mercado-pago" in path:
            gateway = "mercado_pago"
        elif "stripe" in path:
            gateway = "stripe"
        else:
            gateway = "mercado_pago"

    # Ler corpo bruto
    try:
        raw_body = await request.body()
        payload = await request.json()
    except Exception:
        return {"status": "error", "message": "Payload inválido."}

    # Obter assinatura do header
    signature = (
        request.headers.get("x-signature")  # MercadoPago
        or request.headers.get("stripe-signature")  # Stripe
        or ""
    )

    svc = _get_service(session)
    result = await svc.process_webhook(gateway, payload, signature, raw_body)
    return result


# ============================================================
# Helpers
# ============================================================

def _payment_response(p: object) -> PaymentResponse:
    gw = getattr(p, "gateway", "")
    gw_str = gw.value if hasattr(gw, "value") else str(gw)

    pm = getattr(p, "payment_method", None)
    pm_str = pm.value if hasattr(pm, "value") else str(pm) if pm else None

    return PaymentResponse(
        id=getattr(p, "id", ""),
        booking_id=getattr(p, "booking_id", None),
        subscription_id=getattr(p, "subscription_id", None),
        amount=getattr(p, "amount", 0),
        status=getattr(p, "status", ""),
        payment_method=pm_str,
        gateway=gw_str,
        gateway_payment_id=getattr(p, "gateway_payment_id", None),
        gateway_checkout_url=getattr(p, "gateway_checkout_url", None),
        pix_qr_code=getattr(p, "pix_qr_code", None),
        pix_copy_paste=getattr(p, "pix_copy_paste", None),
        pix_expires_at=getattr(p, "pix_expires_at", None),
        paid_at=getattr(p, "paid_at", None),
        refunded_at=getattr(p, "refunded_at", None),
        refunded_amount=getattr(p, "refunded_amount", 0),
        created_at=getattr(p, "created_at", None),
    )
