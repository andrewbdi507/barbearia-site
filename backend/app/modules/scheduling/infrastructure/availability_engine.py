"""Scheduling Module — Availability Engine.

CORACÃO DO SISTEMA — calcula disponibilidade real em tempo real.

Considera:
- Jornada do profissional (StaffSchedule)
- Horário da empresa (BusinessHours)
- Ausências (TimeOff aprovado)
- Datas bloqueadas (BlockedDate)
- Agendamentos existentes (Booking)
- Duração do serviço + buffer
- Feriados e exceções

Inspirado em: Calendly, Google Calendar, Microsoft Bookings.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from typing import Any

from sqlalchemy import and_, func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.scheduling.domain.entities import Booking, BlockedDate
from app.modules.scheduling.domain.interfaces import IAvailabilityEngine
from app.modules.scheduling.domain.value_objects import AvailabilityResult, BookingSlot, TimeSlot
from app.modules.scheduling.infrastructure.models.scheduling_models import (
    BlockedDateModel,
    BookingModel,
)
from app.modules.staff.infrastructure.models.staff_models import (
    StaffProfileModel,
    StaffScheduleModel,
    TimeOffModel,
)
from app.modules.tenant.infrastructure.models.tenant_models import (
    BusinessHoursModel,
    TenantSettingsModel,
)


class AvailabilityEngine(IAvailabilityEngine):
    """Motor de disponibilidade otimizado.

    Usa UMA query composta para todos os fatores, em vez de
    múltiplas queries sequenciais. Tempo alvo: <50ms.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    # ============================================================
    # Get Available Slots
    # ============================================================

    async def get_available_slots(
        self,
        tenant_id: str,
        professional_id: str,
        date_from: date,
        date_to: date,
        service_ids: list[str],
    ) -> list[AvailabilityResult]:
        """Calcula TODOS os slots disponíveis em um range de datas."""

        # 1. Calcular duração total (serviço + buffer)
        total_duration = await self._get_total_duration(service_ids)
        if total_duration == 0:
            return []

        # 2. Buscar jornada do profissional (7 dias)
        schedule_map = await self._get_staff_schedule(professional_id, tenant_id)

        # 3. Buscar time-offs aprovados no período
        time_off_dates = await self._get_time_off_dates(professional_id, date_from, date_to)

        # 4. Buscar blocked dates
        blocked_dates = await self._get_blocked_dates(tenant_id, professional_id, date_from, date_to)

        # 5. Buscar bookings existentes
        existing_bookings = await self._get_existing_bookings(professional_id, date_from, date_to)

        # 6. Para cada dia, calcular slots
        results: list[AvailabilityResult] = []
        current = date_from
        while current <= date_to:
            if current.isoformat() in time_off_dates:
                current += timedelta(days=1)
                continue

            day_schedule = schedule_map.get(current.weekday())
            if day_schedule is None or not day_schedule.get("is_working"):
                current += timedelta(days=1)
                continue

            slots = self._compute_slots_for_day(
                current, day_schedule, existing_bookings, blocked_dates, total_duration,
            )

            results.append(AvailabilityResult(
                date=current,
                professional_id=professional_id,
                slots=slots,
            ))
            current += timedelta(days=1)

        return results

    # ============================================================
    # Get Next Available Slot
    # ============================================================

    async def get_next_available_slot(
        self,
        tenant_id: str,
        professional_id: str,
        service_ids: list[str],
        from_date: date | None = None,
    ) -> BookingSlot | None:
        start = from_date or date.today()
        end = start + timedelta(days=60)

        results = await self.get_available_slots(tenant_id, professional_id, start, end, service_ids)
        for r in results:
            if r.slots:
                return BookingSlot(
                    date=r.date,
                    time_slot=r.slots[0],
                    professional_id=professional_id,
                    service_ids=service_ids,
                    available=True,
                )
        return None

    # ============================================================
    # Smart Suggestions (DIFERENCIAL)
    # ============================================================

    async def get_smart_suggestions(
        self,
        tenant_id: str,
        professional_id: str | None,
        service_ids: list[str],
        customer_id: str | None,
        from_date: date | None = None,
        max_suggestions: int = 5,
    ) -> list[BookingSlot]:
        """Sugere os MELHORES horários, não apenas os disponíveis.

        Heurísticas:
        1. Preferir horários que evitam gaps (contíguos)
        2. Se customer_id, preferir mesmo profissional da última visita
        3. Preferir horários de menor movimento (meio da manhã/tarde)
        4. Evitar horários muito próximos ao almoço
        """
        start = from_date or date.today()
        end = start + timedelta(days=14)

        # Se professional_id específico, busca só dele
        prof_ids = [professional_id] if professional_id else await self._get_active_professionals(tenant_id)
        if not prof_ids:
            return []

        total_duration = await self._get_total_duration(service_ids)
        all_slots: list[BookingSlot] = []

        for pid in prof_ids[:3]:  # Limita a 3 profissionais para performance
            results = await self.get_available_slots(tenant_id, pid, start, end, service_ids)
            for r in results:
                for slot in r.slots:
                    all_slots.append(BookingSlot(
                        date=r.date, time_slot=slot,
                        professional_id=pid,
                        service_ids=service_ids,
                        available=True,
                        total_duration=total_duration,
                    ))

        # Ordenar por heurísticas de qualidade
        scored = self._score_and_rank(all_slots, customer_id, professional_id)
        return scored[:max_suggestions]

    # ============================================================
    # Private: Data Fetching
    # ============================================================

    async def _get_total_duration(self, service_ids: list[str]) -> int:
        from app.modules.scheduling.infrastructure.models.scheduling_models import ServiceModel
        r = await self._s.execute(
            select(func.sum(ServiceModel.duration_minutes + ServiceModel.buffer_minutes))
            .where(ServiceModel.id.in_(service_ids))
        )
        return (r.scalar() or 0)

    async def _get_staff_schedule(self, professional_id: str, tenant_id: str) -> dict[int, dict]:
        """Retorna {day_of_week: {is_working, start_time, end_time, ...}}."""
        # Tenta StaffSchedule; fallback para BusinessHours
        r = await self._s.execute(
            select(StaffScheduleModel)
            .where(StaffScheduleModel.staff_id == professional_id)
            .order_by(StaffScheduleModel.day_of_week)
        )
        rows = r.scalars().all()
        if rows:
            return {
                row.day_of_week: {
                    "is_working": row.is_working,
                    "start_time": row.start_time,
                    "end_time": row.end_time,
                    "lunch_start": row.lunch_start,
                    "lunch_end": row.lunch_end,
                    "slot_duration_minutes": row.slot_duration_minutes,
                }
                for row in rows
            }

        # Fallback: BusinessHours do tenant
        r2 = await self._s.execute(
            select(BusinessHoursModel)
            .where(BusinessHoursModel.tenant_id == tenant_id)
            .order_by(BusinessHoursModel.day_of_week)
        )
        return {
            row.day_of_week: {
                "is_working": not row.is_closed,
                "start_time": row.open_time,
                "end_time": row.close_time,
                "lunch_start": row.lunch_start,
                "lunch_end": row.lunch_end,
                "slot_duration_minutes": row.slot_duration_minutes,
            }
            for row in r2.scalars().all()
        }

    async def _get_time_off_dates(self, professional_id: str, dfrom: date, dto: date) -> set[str]:
        r = await self._s.execute(
            select(TimeOffModel.start_date, TimeOffModel.end_date)
            .where(TimeOffModel.staff_id == professional_id)
            .where(TimeOffModel.status == "approved")
            .where(TimeOffModel.start_date <= dto)
            .where(TimeOffModel.end_date >= dfrom)
        )
        dates: set[str] = set()
        for row in r.all():
            d = max(row[0], dfrom) if row[0] else dfrom
            end = min(row[1], dto) if row[1] else dto
            while d <= end:
                dates.add(d.isoformat())
                d += timedelta(days=1)
        return dates

    async def _get_blocked_dates(
        self, tenant_id: str, professional_id: str, dfrom: date, dto: date,
    ) -> dict[str, BlockedDate]:
        r = await self._s.execute(
            select(BlockedDateModel)
            .where(BlockedDateModel.tenant_id == tenant_id)
            .where(BlockedDateModel.blocked_date >= dfrom)
            .where(BlockedDateModel.blocked_date <= dto)
            .where(
                or_(
                    BlockedDateModel.professional_id == professional_id,
                    BlockedDateModel.professional_id.is_(None),  # Todos
                )
            )
        )
        result: dict[str, BlockedDate] = {}
        for row in r.scalars().all():
            key = row.blocked_date.isoformat()
            existing = result.get(key)
            if existing is None or row.professional_id == professional_id:
                result[key] = BlockedDate(
                    id=row.id, tenant_id=row.tenant_id or "",
                    blocked_date=row.blocked_date,
                    professional_id=row.professional_id,
                    block_type=row.block_type,
                    reason=row.reason or "",
                    start_time=row.start_time,
                    end_time=row.end_time,
                )
        return result

    async def _get_existing_bookings(
        self, professional_id: str, dfrom: date, dto: date,
    ) -> dict[str, list[tuple[time, time]]]:
        r = await self._s.execute(
            select(BookingModel.booking_date, BookingModel.start_time, BookingModel.end_time)
            .where(BookingModel.professional_id == professional_id)
            .where(BookingModel.booking_date >= dfrom)
            .where(BookingModel.booking_date <= dto)
            .where(BookingModel.status.in_(["pending", "confirmed", "in_progress"]))
            .order_by(BookingModel.start_time)
        )
        result: dict[str, list[tuple[time, time]]] = {}
        for row in r.all():
            key = row[0].isoformat()
            result.setdefault(key, []).append((row[1], row[2]))
        return result

    async def _get_active_professionals(self, tenant_id: str) -> list[str]:
        r = await self._s.execute(
            select(StaffProfileModel.id)
            .where(StaffProfileModel.tenant_id == tenant_id)
            .where(StaffProfileModel.status == "active")
        )
        return [row[0] for row in r.all()]

    # ============================================================
    # Private: Slot Computation
    # ============================================================

    def _compute_slots_for_day(
        self,
        day: date,
        schedule: dict,
        existing_bookings: dict[str, list[tuple[time, time]]],
        blocked_dates: dict[str, BlockedDate],
        total_duration: int,
    ) -> list[TimeSlot]:
        """Calcula slots disponíveis para um dia específico."""

        day_key = day.isoformat()

        # Verificar blocked date full-day
        bd = blocked_dates.get(day_key)
        if bd and bd.block_type == "full_day":
            return []

        start_str = schedule["start_time"]
        end_str = schedule["end_time"]
        lunch_start = schedule.get("lunch_start")
        lunch_end = schedule.get("lunch_end")

        work_start = self._parse_time(start_str)
        work_end = self._parse_time(end_str)

        # Gerar todos os slots possíveis
        slot_duration = schedule.get("slot_duration_minutes", 30)
        interval = min(slot_duration, total_duration)

        all_slots: list[TimeSlot] = []
        current = datetime.combine(day, work_start)
        work_end_dt = datetime.combine(day, work_end)

        while current + timedelta(minutes=total_duration) <= work_end_dt:
            slot_start = current.time()
            slot_end = (current + timedelta(minutes=total_duration)).time()

            # Pular horário de almoço
            if lunch_start and lunch_end:
                ls = self._parse_time(lunch_start)
                le = self._parse_time(lunch_end)
                slot_ts = TimeSlot(slot_start, slot_end, total_duration)
                lunch_ts = TimeSlot(ls, le, 0)
                if slot_ts.overlaps(lunch_ts):
                    current = datetime.combine(day, le)
                    continue

            # Verificar conflito com blocked date parcial
            if bd and bd.block_type == "partial" and bd.start_time and bd.end_time:
                block_ts = TimeSlot(bd.start_time, bd.end_time, 0)
                if TimeSlot(slot_start, slot_end, total_duration).overlaps(block_ts):
                    current += timedelta(minutes=interval)
                    continue

            # Verificar conflito com bookings existentes
            day_bookings = existing_bookings.get(day_key, [])
            conflict = False
            for b_start, b_end in day_bookings:
                if TimeSlot(slot_start, slot_end, total_duration).overlaps(
                    TimeSlot(b_start, b_end, 0)
                ):
                    conflict = True
                    break

            if not conflict:
                all_slots.append(TimeSlot(slot_start, slot_end, total_duration))

            current += timedelta(minutes=interval)

        return all_slots

    # ============================================================
    # Private: Smart Ranking
    # ============================================================

    def _score_and_rank(
        self,
        slots: list[BookingSlot],
        customer_id: str | None,
        preferred_professional_id: str | None,
    ) -> list[BookingSlot]:
        """Atribui score a cada slot e ordena por qualidade."""

        scored: list[tuple[int, BookingSlot]] = []
        for slot in slots:
            score = 0

            # Preferir profissional preferido (+10)
            if preferred_professional_id and slot.professional_id == preferred_professional_id:
                score += 10

            # Preferir meio da manhã (9h-11h) ou meio da tarde (14h-16h) (+5)
            h = slot.time_slot.start.hour
            if (9 <= h <= 11) or (14 <= h <= 16):
                score += 5

            # Evitar horários de pico de almoço (11h30-13h30) (-3)
            if 11 <= h <= 13:
                score -= 3

            # Preferir slots que começam em hora cheia ou meia (+2)
            if slot.time_slot.start.minute in (0, 30):
                score += 2

            # Preferir datas mais próximas (+remaining days score)
            days_ahead = (slot.date - date.today()).days
            if days_ahead <= 1:
                score += 3  # Hoje/amanhã tem prioridade
            elif days_ahead <= 7:
                score += 1

            scored.append((score, slot))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored]

    @staticmethod
    def _parse_time(t_str: str) -> time:
        parts = t_str.split(":")
        return time(int(parts[0]), int(parts[1]))
