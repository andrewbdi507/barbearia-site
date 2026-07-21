"""Payment Module — Repository Implementation."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.payment.domain.entities import (
    GatewayConfig,
    Payment,
    PaymentEvent,
    SubscriptionPayment,
)
from app.modules.payment.domain.repository_interfaces import (
    IGatewayConfigRepository,
    IPaymentEventRepository,
    IPaymentRepository,
    ISubscriptionPaymentRepository,
)
from app.modules.payment.infrastructure.models.payment_models import (
    GatewayConfigModel,
    PaymentEventModel,
    PaymentModel,
    SubscriptionPaymentModel,
)


def _payment_to_entity(m: PaymentModel) -> Payment:
    return Payment(
        id=m.id, tenant_id=m.tenant_id or "",
        booking_id=m.booking_id, subscription_id=m.subscription_id,
        customer_id=m.customer_id, amount=m.amount,
        original_amount=m.original_amount, currency=m.currency,
        status=m.status, payment_method=m.payment_method,
        gateway=m.gateway, gateway_payment_id=m.gateway_payment_id,
        gateway_checkout_url=m.gateway_checkout_url,
        pix_qr_code=m.pix_qr_code, pix_copy_paste=m.pix_copy_paste,
        pix_expires_at=m.pix_expires_at,
        idempotency_key=m.idempotency_key,
        deposit_type=m.deposit_type, deposit_value=m.deposit_value,
        paid_at=m.paid_at, refunded_at=m.refunded_at,
        refunded_amount=m.refunded_amount, metadata=m.metadata or {},
        created_at=m.created_at, updated_at=m.updated_at,
    )


def _event_to_entity(m: PaymentEventModel) -> PaymentEvent:
    return PaymentEvent(
        id=m.id, payment_id=m.payment_id,
        event_type=m.event_type, gateway_raw_data=m.gateway_raw_data or {},
        gateway_event_id=m.gateway_event_id,
        ip_address=m.ip_address, metadata=m.metadata or {},
        created_at=m.created_at,
    )


class PaymentRepository(IPaymentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, payment_id: str) -> Payment | None:
        r = await self._s.execute(select(PaymentModel).where(PaymentModel.id == payment_id))
        m = r.scalar_one_or_none()
        return _payment_to_entity(m) if m else None

    async def get_by_gateway_id(self, gateway_payment_id: str) -> Payment | None:
        r = await self._s.execute(
            select(PaymentModel).where(PaymentModel.gateway_payment_id == gateway_payment_id)
        )
        m = r.scalar_one_or_none()
        return _payment_to_entity(m) if m else None

    async def get_by_idempotency_key(self, key: str) -> Payment | None:
        r = await self._s.execute(
            select(PaymentModel).where(PaymentModel.idempotency_key == key)
        )
        m = r.scalar_one_or_none()
        return _payment_to_entity(m) if m else None

    async def create(self, p: Payment) -> Payment:
        m = PaymentModel(
            id=p.id, tenant_id=p.tenant_id,
            booking_id=p.booking_id, subscription_id=p.subscription_id,
            customer_id=p.customer_id, amount=p.amount,
            original_amount=p.original_amount, currency=p.currency,
            status=p.status, payment_method=p.payment_method.value if p.payment_method else None,
            gateway=p.gateway.value if hasattr(p.gateway, 'value') else str(p.gateway),
            idempotency_key=p.idempotency_key,
            deposit_type=p.deposit_type, deposit_value=p.deposit_value,
            metadata=p.metadata,
        )
        self._s.add(m)
        await self._s.flush()
        return _payment_to_entity(m)

    async def update(self, p: Payment) -> Payment:
        m = await self._s.get(PaymentModel, p.id)
        if not m:
            raise ValueError(f"Payment {p.id} not found")
        for f in ("status", "gateway_payment_id", "gateway_checkout_url",
                   "pix_qr_code", "pix_copy_paste", "pix_expires_at",
                   "paid_at", "refunded_at", "refunded_amount", "metadata"):
            setattr(m, f, getattr(p, f))
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _payment_to_entity(m)

    async def update_status(self, payment_id: str, status: str, **kwargs: object) -> None:
        vals: dict = {"status": status, "updated_at": datetime.now(timezone.utc)}
        for k, v in kwargs.items():
            if hasattr(PaymentModel, k) and v is not None:
                vals[k] = v
        await self._s.execute(
            update(PaymentModel).where(PaymentModel.id == payment_id).values(**vals)
        )

    async def list_for_tenant(self, tenant_id: str, *, status: str | None = None, offset: int = 0, limit: int = 50) -> tuple[list[Payment], int]:
        base = select(PaymentModel).where(PaymentModel.tenant_id == tenant_id)
        count_q = select(func.count()).select_from(PaymentModel).where(PaymentModel.tenant_id == tenant_id)
        if status:
            base = base.where(PaymentModel.status == status)
            count_q = count_q.where(PaymentModel.status == status)
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(base.order_by(PaymentModel.created_at.desc()).offset(offset).limit(limit))
        return [_payment_to_entity(m) for m in r.scalars().all()], total

    async def list_for_booking(self, booking_id: str) -> list[Payment]:
        r = await self._s.execute(
            select(PaymentModel).where(PaymentModel.booking_id == booking_id)
        )
        return [_payment_to_entity(m) for m in r.scalars().all()]


class PaymentEventRepository(IPaymentEventRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def log(self, event: PaymentEvent) -> PaymentEvent:
        m = PaymentEventModel(
            id=event.id, payment_id=event.payment_id,
            event_type=event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
            gateway_raw_data=event.gateway_raw_data,
            gateway_event_id=event.gateway_event_id,
            ip_address=event.ip_address, metadata=event.metadata,
        )
        self._s.add(m)
        await self._s.flush()
        return event

    async def get_for_payment(self, payment_id: str) -> list[PaymentEvent]:
        r = await self._s.execute(
            select(PaymentEventModel)
            .where(PaymentEventModel.payment_id == payment_id)
            .order_by(PaymentEventModel.created_at)
        )
        return [_event_to_entity(m) for m in r.scalars().all()]

    async def exists_by_gateway_event_id(self, gateway_event_id: str) -> bool:
        if not gateway_event_id:
            return False
        r = await self._s.execute(
            select(func.count()).select_from(PaymentEventModel)
            .where(PaymentEventModel.gateway_event_id == gateway_event_id)
        )
        return (r.scalar() or 0) > 0


class GatewayConfigRepository(IGatewayConfigRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_for_tenant(self, tenant_id: str, gateway: str) -> GatewayConfig | None:
        r = await self._s.execute(
            select(GatewayConfigModel).where(
                GatewayConfigModel.tenant_id == tenant_id,
                GatewayConfigModel.gateway == gateway,
            )
        )
        m = r.scalar_one_or_none()
        if not m:
            return None
        return GatewayConfig(
            id=m.id, tenant_id=m.tenant_id or "", gateway=m.gateway,
            is_active=m.is_active, api_key_encrypted=m.api_key_encrypted,
            webhook_secret_encrypted=m.webhook_secret_encrypted,
            public_key=m.public_key, settings=m.settings or {},
            created_at=m.created_at,
        )

    async def upsert(self, config: GatewayConfig) -> GatewayConfig:
        r = await self._s.execute(
            select(GatewayConfigModel).where(
                GatewayConfigModel.tenant_id == config.tenant_id,
                GatewayConfigModel.gateway == config.gateway.value if hasattr(config.gateway, 'value') else str(config.gateway),
            )
        )
        m = r.scalar_one_or_none()
        if m:
            m.api_key_encrypted = config.api_key_encrypted
            m.webhook_secret_encrypted = config.webhook_secret_encrypted
            m.public_key = config.public_key
            m.is_active = config.is_active
            m.settings = config.settings
        else:
            m = GatewayConfigModel(
                id=config.id, tenant_id=config.tenant_id,
                gateway=config.gateway.value if hasattr(config.gateway, 'value') else str(config.gateway),
                api_key_encrypted=config.api_key_encrypted,
                webhook_secret_encrypted=config.webhook_secret_encrypted,
                public_key=config.public_key, is_active=config.is_active,
                settings=config.settings,
            )
            self._s.add(m)
        await self._s.flush()
        return config


class SubscriptionPaymentRepository(ISubscriptionPaymentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def create(self, sp: SubscriptionPayment) -> SubscriptionPayment:
        m = SubscriptionPaymentModel(
            id=sp.id, tenant_id=sp.tenant_id,
            subscription_id=sp.subscription_id, payment_id=sp.payment_id,
            amount=sp.amount, billing_period_start=sp.billing_period_start,
            billing_period_end=sp.billing_period_end,
            status=sp.status, attempt_number=sp.attempt_number,
        )
        self._s.add(m)
        await self._s.flush()
        return sp

    async def list_for_subscription(self, subscription_id: str) -> list[SubscriptionPayment]:
        r = await self._s.execute(
            select(SubscriptionPaymentModel)
            .where(SubscriptionPaymentModel.subscription_id == subscription_id)
            .order_by(SubscriptionPaymentModel.created_at.desc())
        )
        return [
            SubscriptionPayment(
                id=m.id, tenant_id=m.tenant_id or "",
                subscription_id=m.subscription_id, payment_id=m.payment_id,
                amount=m.amount, billing_period_start=m.billing_period_start,
                billing_period_end=m.billing_period_end,
                status=m.status, attempt_number=m.attempt_number,
                created_at=m.created_at,
            )
            for m in r.scalars().all()
        ]
