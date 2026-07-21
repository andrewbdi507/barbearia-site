"""Payment Module — Repository Interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.payment.domain.entities import (
    GatewayConfig,
    Payment,
    PaymentEvent,
    SubscriptionPayment,
)


class IPaymentRepository(ABC):
    @abstractmethod
    async def get_by_id(self, payment_id: str) -> Payment | None: ...
    @abstractmethod
    async def get_by_gateway_id(self, gateway_payment_id: str) -> Payment | None: ...
    @abstractmethod
    async def get_by_idempotency_key(self, key: str) -> Payment | None: ...
    @abstractmethod
    async def create(self, payment: Payment) -> Payment: ...
    @abstractmethod
    async def update(self, payment: Payment) -> Payment: ...
    @abstractmethod
    async def update_status(self, payment_id: str, status: str, **kwargs: object) -> None: ...
    @abstractmethod
    async def list_for_tenant(self, tenant_id: str, *, status: str | None = None, offset: int = 0, limit: int = 50) -> tuple[list[Payment], int]: ...
    @abstractmethod
    async def list_for_booking(self, booking_id: str) -> list[Payment]: ...


class IPaymentEventRepository(ABC):
    @abstractmethod
    async def log(self, event: PaymentEvent) -> PaymentEvent: ...
    @abstractmethod
    async def get_for_payment(self, payment_id: str) -> list[PaymentEvent]: ...
    @abstractmethod
    async def exists_by_gateway_event_id(self, gateway_event_id: str) -> bool: ...


class IGatewayConfigRepository(ABC):
    @abstractmethod
    async def get_for_tenant(self, tenant_id: str, gateway: str) -> GatewayConfig | None: ...
    @abstractmethod
    async def upsert(self, config: GatewayConfig) -> GatewayConfig: ...


class ISubscriptionPaymentRepository(ABC):
    @abstractmethod
    async def create(self, sp: SubscriptionPayment) -> SubscriptionPayment: ...
    @abstractmethod
    async def list_for_subscription(self, subscription_id: str) -> list[SubscriptionPayment]: ...
