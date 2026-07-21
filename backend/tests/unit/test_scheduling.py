"""Scheduling Module — Tests.

Cobertura: entities, state machine, availability, booking, DTOs.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from app.modules.scheduling.domain.entities import (
    BlockedDate,
    Booking,
    BookingStatusLog,
    Service,
    ServiceCategory,
    WaitlistEntry,
)
from app.modules.scheduling.domain.enums import (
    BlockType,
    BookingSource,
    BookingStatus,
    WaitlistStatus,
)
from app.modules.scheduling.domain.value_objects import ServicePricing, TimeSlot


# ============================================================
# TimeSlot Tests
# ============================================================

class TestTimeSlot:
    def test_valid(self) -> None:
        ts = TimeSlot(time(9, 0), time(10, 0), 60)
        assert ts.start == time(9, 0)

    def test_invalid_start_after_end(self) -> None:
        with pytest.raises(ValueError):
            TimeSlot(time(10, 0), time(9, 0))

    def test_overlaps_true(self) -> None:
        a = TimeSlot(time(9, 0), time(10, 0))
        b = TimeSlot(time(9, 30), time(10, 30))
        assert a.overlaps(b)

    def test_overlaps_false(self) -> None:
        a = TimeSlot(time(9, 0), time(10, 0))
        b = TimeSlot(time(10, 0), time(11, 0))
        assert not a.overlaps(b)

    def test_overlaps_contained(self) -> None:
        a = TimeSlot(time(9, 0), time(12, 0))
        b = TimeSlot(time(10, 0), time(11, 0))
        assert a.overlaps(b)


# ============================================================
# ServicePricing Tests
# ============================================================

class TestServicePricing:
    def test_effective_price_base(self) -> None:
        p = ServicePricing(base_price=5000)
        assert p.effective_price == 5000

    def test_effective_price_promotional(self) -> None:
        p = ServicePricing(base_price=5000, promotional_price=3500)
        assert p.effective_price == 3500

    def test_format_brl(self) -> None:
        p = ServicePricing(base_price=4590)
        assert "45" in p.format_brl()


# ============================================================
# Booking State Machine Tests
# ============================================================

class TestBookingStateMachine:
    def _make_booking(self, status: BookingStatus = BookingStatus.PENDING) -> Booking:
        return Booking(
            id="b1", tenant_id="t1", professional_id="p1",
            booking_date=date.today(),
            start_time=time(9, 0), end_time=time(10, 0),
            status=status,
        )

    def test_confirm_from_pending(self) -> None:
        b = self._make_booking(BookingStatus.PENDING)
        b.confirm()
        assert b.status == BookingStatus.CONFIRMED

    def test_start_service_from_confirmed(self) -> None:
        b = self._make_booking(BookingStatus.CONFIRMED)
        b.start_service()
        assert b.status == BookingStatus.IN_PROGRESS
        assert b.checked_in_at is not None

    def test_complete_from_in_progress(self) -> None:
        b = self._make_booking(BookingStatus.IN_PROGRESS)
        b.complete()
        assert b.status == BookingStatus.COMPLETED
        assert b.completed_at is not None

    def test_cancel_from_pending(self) -> None:
        b = self._make_booking(BookingStatus.PENDING)
        b.cancel("Cliente desistiu", "u1")
        assert b.status == BookingStatus.CANCELLED
        assert b.cancellation_reason == "Cliente desistiu"

    def test_cannot_cancel_completed(self) -> None:
        b = self._make_booking(BookingStatus.COMPLETED)
        with pytest.raises(ValueError):
            b.cancel("teste")

    def test_mark_no_show_from_confirmed(self) -> None:
        b = self._make_booking(BookingStatus.CONFIRMED)
        b.mark_no_show()
        assert b.status == BookingStatus.NO_SHOW

    def test_reschedule(self) -> None:
        b = self._make_booking(BookingStatus.CONFIRMED)
        b.reschedule_to("b_new")
        assert b.status == BookingStatus.RESCHEDULED
        assert b.rescheduled_to_id == "b_new"

    def test_can_be_modified_pending(self) -> None:
        b = self._make_booking(BookingStatus.PENDING)
        assert b.can_be_modified()

    def test_cannot_be_modified_completed(self) -> None:
        b = self._make_booking(BookingStatus.COMPLETED)
        assert not b.can_be_modified()


# ============================================================
# Service Entity
# ============================================================

class TestService:
    def test_total_duration_includes_buffer(self) -> None:
        s = Service(
            id="s1", tenant_id="t1", name="Corte",
            duration_minutes=30, buffer_minutes=5,
        )
        assert s.total_duration == 35

    def test_effective_price(self) -> None:
        s = Service(
            id="s1", tenant_id="t1", name="Corte",
            pricing=ServicePricing(base_price=4500),
        )
        assert s.effective_price == 4500


# ============================================================
# Waitlist
# ============================================================

class TestWaitlist:
    def test_notify(self) -> None:
        w = WaitlistEntry(id="w1", tenant_id="t1")
        w.notify(expires_hours=24)
        assert w.status == WaitlistStatus.NOTIFIED
        assert w.notified_at is not None
        assert w.expires_at is not None


# ============================================================
# Availability Engine (Unit)
# ============================================================

class TestAvailabilityEngine:
    def test_parse_time(self) -> None:
        from app.modules.scheduling.infrastructure.availability_engine import AvailabilityEngine
        t = AvailabilityEngine._parse_time("14:30")
        assert t == time(14, 30)

    def test_compute_slots_empty_when_full_day_blocked(self) -> None:
        from app.modules.scheduling.infrastructure.availability_engine import AvailabilityEngine
        engine = AvailabilityEngine.__new__(AvailabilityEngine)
        schedule = {"start_time": "09:00", "end_time": "18:00", "slot_duration_minutes": 30}
        blocked = {"2026-07-20": BlockedDate(
            id="bd1", tenant_id="t1", blocked_date=date(2026, 7, 20),
            block_type="full_day",
        )}
        slots = engine._compute_slots_for_day(
            date(2026, 7, 20), schedule, {}, blocked, 60,
        )
        assert len(slots) == 0

    def test_compute_slots_skips_existing_bookings(self) -> None:
        from app.modules.scheduling.infrastructure.availability_engine import AvailabilityEngine
        engine = AvailabilityEngine.__new__(AvailabilityEngine)
        schedule = {"start_time": "09:00", "end_time": "18:00", "slot_duration_minutes": 30}
        bookings = {"2026-07-20": [(time(9, 0), time(10, 0))]}
        slots = engine._compute_slots_for_day(
            date(2026, 7, 20), schedule, bookings, {}, 60,
        )
        # Slot 09:00 deve estar ocupado
        slot_starts = [s.start for s in slots]
        assert time(9, 0) not in slot_starts


# ============================================================
# DTO Validation
# ============================================================

class TestDTOs:
    def test_service_create(self) -> None:
        from app.modules.scheduling.application.dto import ServiceCreateRequest
        req = ServiceCreateRequest(
            name="Corte Social", duration_minutes=45, base_price=5000, buffer_minutes=10,
        )
        assert req.name == "Corte Social"
        assert req.buffer_minutes == 10

    def test_booking_create(self) -> None:
        from app.modules.scheduling.application.dto import BookingCreateRequest
        req = BookingCreateRequest(
            professional_id="p1", booking_date=date.today(),
            start_time="09:00", service_ids=["s1"],
            idempotency_key="idem-abc123",
        )
        assert req.idempotency_key == "idem-abc123"

    def test_blocked_date_create(self) -> None:
        from app.modules.scheduling.application.dto import BlockedDateCreateRequest
        req = BlockedDateCreateRequest(
            blocked_date=date(2026, 12, 25),
            reason="Natal", block_type="full_day",
        )
        assert req.reason == "Natal"

    def test_service_invalid_duration(self) -> None:
        from app.modules.scheduling.application.dto import ServiceCreateRequest
        import pydantic
        with pytest.raises(pydantic.ValidationError):
            ServiceCreateRequest(name="Test", duration_minutes=0)
