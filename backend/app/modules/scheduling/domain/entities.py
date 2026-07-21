"""Scheduling Module — Domain Entities.

Entidades puras — Service, ServiceCategory, Booking, BookingStatusLog,
BlockedDate, Waitlist, ProfessionalService.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timezone
from typing import Any
from uuid import uuid4

from app.modules.scheduling.domain.enums import (
    BlockType,
    BookingSource,
    BookingStatus,
    WaitlistStatus,
)
from app.modules.scheduling.domain.value_objects import ServicePricing


@dataclass
class ServiceCategory:
    """Categoria de serviços configurável."""

    id: str
    tenant_id: str
    name: str
    description: str = ""
    color_tag: str = "#cccccc"
    is_active: bool = True
    sort_order: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Service:
    """Serviço oferecido pelo tenant.

    Aggregate Root do catálogo de serviços.
    """

    id: str
    tenant_id: str
    name: str
    category_id: str | None = None
    description: str = ""
    duration_minutes: int = 30
    buffer_minutes: int = 0  # Tempo de limpeza/preparação entre clientes
    pricing: ServicePricing = field(default_factory=ServicePricing)
    color_tag: str = "#cccccc"
    image_url: str | None = None
    is_active: bool = True
    sort_order: int = 0
    min_advance_minutes: int = 0  # 0 = sem restrição
    max_advance_days: int = 90  # 0 = sem limite
    notes: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = None

    @property
    def total_duration(self) -> int:
        """Duração total incluindo buffer."""
        return self.duration_minutes + self.buffer_minutes

    @property
    def base_price(self) -> int:
        return self.pricing.base_price

    @property
    def effective_price(self) -> int:
        return self.pricing.effective_price


@dataclass
class ProfessionalService:
    """Associação N:N — serviço que um profissional realiza.

    Permite customizar preço e duração por profissional.
    """

    id: str
    tenant_id: str
    professional_id: str  # FK → StaffProfile
    service_id: str
    custom_price: int | None = None
    custom_duration: int | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def effective_price(self) -> int:
        return self.custom_price if self.custom_price is not None else 0

    @property
    def effective_duration(self) -> int:
        return self.custom_duration if self.custom_duration is not None else 0


@dataclass
class Booking:
    """Aggregate Root — Agendamento.

    Entidade central do sistema. Gerencia todo o ciclo de vida.
    """

    id: str
    tenant_id: str
    professional_id: str
    booking_date: date
    start_time: time
    end_time: time
    status: BookingStatus = BookingStatus.PENDING
    customer_id: str | None = None  # FK → Customer (guest se null)
    guest_name: str | None = None
    guest_phone: str | None = None
    guest_email: str | None = None
    notes: str | None = None
    total_amount: int = 0  # centavos
    total_duration_minutes: int = 0
    discount_amount: int = 0
    source: BookingSource = BookingSource.WEBSITE
    idempotency_key: str | None = None  # Anti double-booking
    created_by: str | None = None
    cancelled_at: datetime | None = None
    cancelled_by: str | None = None
    cancellation_reason: str | None = None
    checked_in_at: datetime | None = None
    completed_at: datetime | None = None
    rescheduled_from_id: str | None = None  # Booking original
    rescheduled_to_id: str | None = None  # Novo booking
    metadata: dict[str, Any] = field(default_factory=dict)
    service_ids: list[str] = field(default_factory=list)  # IDs dos serviços
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # ============================================================
    # State Machine
    # ============================================================

    def confirm(self) -> None:
        if self.status not in {BookingStatus.PENDING, BookingStatus.WAITLIST}:
            raise ValueError(f"Não pode confirmar booking com status '{self.status}'")
        self.status = BookingStatus.CONFIRMED
        self.updated_at = datetime.now(timezone.utc)

    def start_service(self) -> None:
        if self.status != BookingStatus.CONFIRMED:
            raise ValueError(f"Não pode iniciar booking com status '{self.status}'")
        self.status = BookingStatus.IN_PROGRESS
        self.checked_in_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def complete(self) -> None:
        if self.status != BookingStatus.IN_PROGRESS:
            raise ValueError(f"Não pode completar booking com status '{self.status}'")
        self.status = BookingStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def cancel(self, reason: str, cancelled_by: str | None = None) -> None:
        if self.status in {BookingStatus.COMPLETED, BookingStatus.CANCELLED, BookingStatus.RESCHEDULED}:
            raise ValueError(f"Não pode cancelar booking com status '{self.status}'")
        self.status = BookingStatus.CANCELLED
        self.cancelled_at = datetime.now(timezone.utc)
        self.cancelled_by = cancelled_by
        self.cancellation_reason = reason
        self.updated_at = datetime.now(timezone.utc)

    def mark_no_show(self) -> None:
        if self.status not in {BookingStatus.CONFIRMED, BookingStatus.PENDING}:
            raise ValueError(f"Não pode marcar no-show com status '{self.status}'")
        self.status = BookingStatus.NO_SHOW
        self.updated_at = datetime.now(timezone.utc)

    def reschedule_to(self, new_booking_id: str) -> None:
        if self.status in {BookingStatus.CANCELLED, BookingStatus.COMPLETED, BookingStatus.RESCHEDULED}:
            raise ValueError(f"Não pode reagendar booking com status '{self.status}'")
        self.status = BookingStatus.RESCHEDULED
        self.rescheduled_to_id = new_booking_id
        self.updated_at = datetime.now(timezone.utc)

    def can_be_modified(self) -> bool:
        return self.status in {BookingStatus.PENDING, BookingStatus.CONFIRMED}

    @property
    def is_guest(self) -> bool:
        return self.customer_id is None


@dataclass
class BookingStatusLog:
    """Registro imutável de transição de status (append-only)."""

    id: str
    booking_id: str
    from_status: str | None = None
    to_status: str = ""
    changed_by: str | None = None
    ip_address: str | None = None
    notes: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class BlockedDate:
    """Data bloqueada na agenda (feriado, manutenção, evento)."""

    id: str
    tenant_id: str
    blocked_date: date
    professional_id: str | None = None  # None = todos
    block_type: BlockType = BlockType.FULL_DAY
    reason: str = ""
    start_time: time | None = None  # Para bloqueios parciais
    end_time: time | None = None
    is_recurring: bool = False
    recurring_pattern: str | None = None
    recurring_until: date | None = None
    created_by: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class WaitlistEntry:
    """Entrada na lista de espera."""

    id: str
    tenant_id: str
    customer_id: str | None = None
    guest_name: str | None = None
    guest_phone: str | None = None
    professional_id: str | None = None  # Preferência de profissional
    service_id: str | None = None
    desired_date: date | None = None
    desired_period: str = "any"  # morning, afternoon, evening, any
    status: WaitlistStatus = WaitlistStatus.WAITING
    position: int = 0
    notified_at: datetime | None = None
    expires_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def notify(self, expires_hours: int = 24) -> None:
        self.status = WaitlistStatus.NOTIFIED
        self.notified_at = datetime.now(timezone.utc)
        self.expires_at = datetime.now(timezone.utc) + __import__("datetime").timedelta(hours=expires_hours)

    def promote_to_booking(self) -> None:
        self.status = WaitlistStatus.BOOKED
