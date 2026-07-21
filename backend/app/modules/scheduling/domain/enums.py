"""Scheduling Module — Domain Enums.

Define TODOS os estados do módulo de agendamento.
"""

from __future__ import annotations

from enum import StrEnum


class BookingStatus(StrEnum):
    """Máquina de estados completa do agendamento.

    pending → confirmed → in_progress → completed
                   ↓            ↓
              cancelled      no_show
                   ↓
              rescheduled (vira novo booking)
    """

    PENDING = "pending"
    WAITING_PAYMENT = "waiting_payment"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"
    WAITLIST = "waitlist"


class BookingSource(StrEnum):
    """Origem/canal do agendamento."""

    WEBSITE = "website"
    ADMIN = "admin"
    RECEPTIONIST = "receptionist"
    INSTAGRAM = "instagram"
    WHATSAPP = "whatsapp"
    PHONE = "phone"
    WALK_IN = "walk_in"
    API = "api"


class BlockType(StrEnum):
    """Tipo de bloqueio na agenda."""

    FULL_DAY = "full_day"
    PARTIAL = "partial"
    RECURRING = "recurring"


class WaitlistStatus(StrEnum):
    """Status da lista de espera."""

    WAITING = "waiting"
    NOTIFIED = "notified"
    ACCEPTED = "accepted"  # Cliente aceitou a vaga
    DECLINED = "declined"
    BOOKED = "booked"  # Promovido a booking
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class RecurringPattern(StrEnum):
    """Padrão de recorrência para bloqueios."""

    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
