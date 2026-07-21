"""Scheduling Module — Value Objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Any


@dataclass(frozen=True, slots=True)
class TimeSlot:
    """Faixa de horário — imutável, comparável."""

    start: time
    end: time
    duration_minutes: int = 30

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError(f"start ({self.start}) deve ser < end ({self.end})")

    @property
    def duration(self) -> timedelta:
        return timedelta(
            hours=self.end.hour - self.start.hour,
            minutes=self.end.minute - self.start.minute,
        )

    def overlaps(self, other: TimeSlot) -> bool:
        return self.start < other.end and other.start < self.end

    def __str__(self) -> str:
        return f"{self.start.strftime('%H:%M')}-{self.end.strftime('%H:%M')}"


@dataclass(frozen=True, slots=True)
class ServicePricing:
    """Preço do serviço — imutável."""

    base_price: int = 0  # centavos
    promotional_price: int | None = None
    requires_deposit: bool = False
    deposit_value: int = 0  # centavos

    @property
    def effective_price(self) -> int:
        """Preço efetivo (promocional se disponível)."""
        if self.promotional_price is not None and self.promotional_price > 0:
            return self.promotional_price
        return self.base_price

    def format_brl(self) -> str:
        p = self.effective_price / 100
        return f"R$ {p:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@dataclass(frozen=True, slots=True)
class BookingSlot:
    """Slot completo de agendamento com dados agregados."""

    date: date
    time_slot: TimeSlot
    professional_id: str
    professional_name: str = ""
    service_ids: list[str] = field(default_factory=list)
    available: bool = True
    total_price: int = 0
    total_duration: int = 0  # minutos (serviço + buffer)
    suggested: bool = False  # Smart suggestion flag


@dataclass(frozen=True, slots=True)
class AvailabilityResult:
    """Resultado do cálculo de disponibilidade."""

    date: date
    professional_id: str
    slots: list[TimeSlot] = field(default_factory=list)
    blocked_reasons: dict[str, str] = field(default_factory=dict)
