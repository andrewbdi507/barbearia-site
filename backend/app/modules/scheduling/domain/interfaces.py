"""Scheduling Module — Repository Interfaces (Ports)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from app.modules.scheduling.domain.entities import (
    BlockedDate,
    Booking,
    BookingStatusLog,
    ProfessionalService,
    Service,
    ServiceCategory,
    WaitlistEntry,
)
from app.modules.scheduling.domain.value_objects import AvailabilityResult, BookingSlot


class IServiceRepository(ABC):
    @abstractmethod
    async def get_by_id(self, service_id: str) -> Service | None: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: str, *, category_id: str | None = None, active_only: bool = True) -> list[Service]: ...
    @abstractmethod
    async def create(self, service: Service) -> Service: ...
    @abstractmethod
    async def update(self, service: Service) -> Service: ...
    @abstractmethod
    async def soft_delete(self, service_id: str) -> None: ...


class IServiceCategoryRepository(ABC):
    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[ServiceCategory]: ...
    @abstractmethod
    async def create(self, category: ServiceCategory) -> ServiceCategory: ...
    @abstractmethod
    async def update(self, category: ServiceCategory) -> ServiceCategory: ...
    @abstractmethod
    async def delete(self, category_id: str) -> None: ...


class IProfessionalServiceRepository(ABC):
    @abstractmethod
    async def get_services_for_professional(self, professional_id: str) -> list[ProfessionalService]: ...
    @abstractmethod
    async def get_professionals_for_service(self, service_id: str) -> list[ProfessionalService]: ...
    @abstractmethod
    async def upsert_batch(self, professional_id: str, services: list[ProfessionalService]) -> list[ProfessionalService]: ...
    @abstractmethod
    async def remove(self, professional_service_id: str) -> None: ...


class IBookingRepository(ABC):
    @abstractmethod
    async def get_by_id(self, booking_id: str) -> Booking | None: ...
    @abstractmethod
    async def get_by_idempotency_key(self, key: str) -> Booking | None: ...
    @abstractmethod
    async def create(self, booking: Booking) -> Booking: ...
    @abstractmethod
    async def update(self, booking: Booking) -> Booking: ...
    @abstractmethod
    async def update_status(self, booking_id: str, status: str, **kwargs: object) -> None: ...
    @abstractmethod
    async def list_for_tenant(
        self, tenant_id: str, *, date_from: date | None = None, date_to: date | None = None,
        professional_id: str | None = None, status: str | None = None,
        offset: int = 0, limit: int = 50,
    ) -> tuple[list[Booking], int]: ...
    @abstractmethod
    async def list_for_professional(
        self, professional_id: str, *, date_from: date | None = None, date_to: date | None = None,
    ) -> list[Booking]: ...
    @abstractmethod
    async def get_bookings_for_date_range(
        self, tenant_id: str, professional_id: str, start_date: date, end_date: date,
    ) -> list[Booking]: ...
    @abstractmethod
    async def count_in_period(self, tenant_id: str, start_date: date, end_date: date) -> int: ...


class IBookingStatusLogRepository(ABC):
    @abstractmethod
    async def log(self, entry: BookingStatusLog) -> BookingStatusLog: ...
    @abstractmethod
    async def get_for_booking(self, booking_id: str) -> list[BookingStatusLog]: ...


class IBlockedDateRepository(ABC):
    @abstractmethod
    async def get_for_tenant(self, tenant_id: str, *, date_from: date | None = None, date_to: date | None = None) -> list[BlockedDate]: ...
    @abstractmethod
    async def get_for_professional(self, professional_id: str, date_from: date, date_to: date) -> list[BlockedDate]: ...
    @abstractmethod
    async def create(self, blocked: BlockedDate) -> BlockedDate: ...
    @abstractmethod
    async def delete(self, blocked_id: str) -> None: ...
    @abstractmethod
    async def is_date_blocked(self, tenant_id: str, professional_id: str | None, check_date: date) -> bool: ...


class IWaitlistRepository(ABC):
    @abstractmethod
    async def get_by_id(self, entry_id: str) -> WaitlistEntry | None: ...
    @abstractmethod
    async def create(self, entry: WaitlistEntry) -> WaitlistEntry: ...
    @abstractmethod
    async def update_status(self, entry_id: str, status: str) -> None: ...
    @abstractmethod
    async def get_next_in_line(self, professional_id: str, desired_date: date) -> WaitlistEntry | None: ...
    @abstractmethod
    async def list_for_tenant(self, tenant_id: str, *, status: str | None = None) -> list[WaitlistEntry]: ...


class IAvailabilityEngine(ABC):
    """Motor de cálculo de disponibilidade — coração do sistema."""

    @abstractmethod
    async def get_available_slots(
        self,
        tenant_id: str,
        professional_id: str,
        date_from: date,
        date_to: date,
        service_ids: list[str],
    ) -> list[AvailabilityResult]: ...

    @abstractmethod
    async def get_next_available_slot(
        self,
        tenant_id: str,
        professional_id: str,
        service_ids: list[str],
        from_date: date | None = None,
    ) -> BookingSlot | None: ...

    @abstractmethod
    async def get_smart_suggestions(
        self,
        tenant_id: str,
        professional_id: str | None,
        service_ids: list[str],
        customer_id: str | None,
        from_date: date | None = None,
        max_suggestions: int = 5,
    ) -> list[BookingSlot]: ...
