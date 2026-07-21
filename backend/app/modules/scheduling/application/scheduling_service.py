"""Scheduling Module — Application Service.

Orquestra TODOS os casos de uso do agendamento:
- Catálogo (serviços, categorias)
- Associação profissional-serviço
- Agendamentos (CRUD, state machine, idempotency)
- Disponibilidade (availability engine)
- Bloqueios
- Lista de espera (auto-promotion)
- Auditoria (status logs)
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from typing import Any
from uuid import uuid4

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.scheduling.domain.entities import (
    BlockedDate,
    Booking,
    BookingStatusLog,
    ProfessionalService,
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
from app.modules.scheduling.domain.interfaces import (
    IAvailabilityEngine,
    IBlockedDateRepository,
    IBookingRepository,
    IBookingStatusLogRepository,
    IProfessionalServiceRepository,
    IServiceCategoryRepository,
    IServiceRepository,
    IWaitlistRepository,
)
from app.modules.scheduling.domain.value_objects import ServicePricing


class SchedulingService:
    """Serviço de orquestração de agendamentos."""

    def __init__(
        self,
        service_repo: IServiceRepository,
        category_repo: IServiceCategoryRepository,
        prof_svc_repo: IProfessionalServiceRepository,
        booking_repo: IBookingRepository,
        status_log_repo: IBookingStatusLogRepository,
        blocked_repo: IBlockedDateRepository,
        waitlist_repo: IWaitlistRepository,
        availability: IAvailabilityEngine,
    ) -> None:
        self._services = service_repo
        self._categories = category_repo
        self._prof_svc = prof_svc_repo
        self._bookings = booking_repo
        self._logs = status_log_repo
        self._blocked = blocked_repo
        self._waitlist = waitlist_repo
        self._availability = availability

    # ============================================================
    # Service Catalog
    # ============================================================

    async def list_services(self, tenant_id: str, *, category_id: str | None = None, active_only: bool = True) -> list[Service]:
        return await self._services.list_by_tenant(tenant_id, category_id=category_id, active_only=active_only)

    async def get_service(self, service_id: str) -> Service:
        s = await self._services.get_by_id(service_id)
        if s is None:
            raise NotFoundError(message="Serviço não encontrado.")
        return s

    async def create_service(self, tenant_id: str, **kwargs: object) -> Service:
        svc = Service(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            category_id=str(kwargs.get("category_id", "")) if kwargs.get("category_id") else None,
            description=str(kwargs.get("description", "")),
            duration_minutes=int(kwargs.get("duration_minutes", 30)),
            buffer_minutes=int(kwargs.get("buffer_minutes", 0)),
            pricing=ServicePricing(
                base_price=int(kwargs.get("base_price", 0)),
                promotional_price=kwargs.get("promotional_price"),
            ),
            color_tag=str(kwargs.get("color_tag", "#cccccc")),
            is_active=bool(kwargs.get("is_active", True)),
            sort_order=int(kwargs.get("sort_order", 0)),
            min_advance_minutes=int(kwargs.get("min_advance_minutes", 0)),
            max_advance_days=int(kwargs.get("max_advance_days", 90)),
            notes=str(kwargs.get("notes", "")) if kwargs.get("notes") else None,
        )
        return await self._services.create(svc)

    async def update_service(self, service_id: str, **kwargs: object) -> Service:
        existing = await self.get_service(service_id)
        for k, v in kwargs.items():
            if hasattr(existing, k) and v is not None:
                setattr(existing, k, v)
        return await self._services.update(existing)

    async def delete_service(self, service_id: str) -> None:
        await self._services.soft_delete(service_id)

    # ============================================================
    # Categories
    # ============================================================

    async def list_categories(self, tenant_id: str) -> list[ServiceCategory]:
        return await self._categories.list_by_tenant(tenant_id)

    async def create_category(self, tenant_id: str, **kwargs: object) -> ServiceCategory:
        cat = ServiceCategory(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            description=str(kwargs.get("description", "")),
            color_tag=str(kwargs.get("color_tag", "#cccccc")),
            sort_order=int(kwargs.get("sort_order", 0)),
        )
        return await self._categories.create(cat)

    async def update_category(self, category_id: str, **kwargs: object) -> ServiceCategory:
        existing = await self._categories.list_by_tenant("")
        cat = next((c for c in existing if c.id == category_id), None)
        if cat is None:
            raise NotFoundError(message="Categoria não encontrada.")
        for k, v in kwargs.items():
            if hasattr(cat, k) and v is not None:
                setattr(cat, k, v)
        return await self._categories.update(cat)

    async def delete_category(self, category_id: str) -> None:
        await self._categories.delete(category_id)

    # ============================================================
    # Professional ↔ Service
    # ============================================================

    async def link_professional_services(
        self, tenant_id: str, professional_id: str, links: list[dict],
    ) -> list[ProfessionalService]:
        entities = [
            ProfessionalService(
                id=str(uuid4()), tenant_id=tenant_id,
                professional_id=professional_id,
                service_id=str(link["service_id"]),
                custom_price=link.get("custom_price"),
                custom_duration=link.get("custom_duration"),
                is_active=link.get("is_active", True),
            )
            for link in links
        ]
        return await self._prof_svc.upsert_batch(professional_id, entities)

    async def get_professional_services(self, professional_id: str) -> list[ProfessionalService]:
        return await self._prof_svc.get_services_for_professional(professional_id)

    # ============================================================
    # Availability
    # ============================================================

    async def get_availability(
        self, tenant_id: str, professional_id: str,
        date_from: date, date_to: date, service_ids: list[str],
    ) -> list[dict]:
        results = await self._availability.get_available_slots(
            tenant_id, professional_id, date_from, date_to, service_ids,
        )
        return [
            {
                "date": r.date.isoformat(),
                "professional_id": r.professional_id,
                "slots": [
                    {"start_time": s.start.strftime("%H:%M"), "end_time": s.end.strftime("%H:%M"),
                     "duration_minutes": s.duration_minutes}
                    for s in r.slots
                ],
            }
            for r in results
        ]

    async def get_smart_suggestions(
        self, tenant_id: str, professional_id: str | None,
        service_ids: list[str], customer_id: str | None = None,
        from_date: date | None = None, max_suggestions: int = 5,
    ) -> list[dict]:
        slots = await self._availability.get_smart_suggestions(
            tenant_id, professional_id, service_ids, customer_id, from_date, max_suggestions,
        )
        return [
            {
                "date": s.date.isoformat(), "start_time": s.time_slot.start.strftime("%H:%M"),
                "end_time": s.time_slot.end.strftime("%H:%M"),
                "professional_id": s.professional_id,
                "professional_name": s.professional_name,
                "total_price": s.total_price, "total_duration": s.total_duration,
                "suggested": s.suggested,
            }
            for s in slots
        ]

    # ============================================================
    # Bookings
    # ============================================================

    async def create_booking(
        self, tenant_id: str, actor_id: str | None, **kwargs: object,
    ) -> Booking:
        """Cria agendamento com validação completa + idempotency."""

        # 1. Idempotency check
        idemp_key = str(kwargs.get("idempotency_key", ""))
        if idemp_key:
            existing = await self._bookings.get_by_idempotency_key(idemp_key)
            if existing:
                return existing

        professional_id = str(kwargs["professional_id"])
        service_ids = list(kwargs.get("service_ids", []))
        booking_date = kwargs["booking_date"]
        start_str = str(kwargs["start_time"])

        # Parse start_time
        parts = start_str.split(":")
        start_time = time(int(parts[0]), int(parts[1]))

        # 2. Calcular duração total
        total_dur = 0
        total_price = 0
        for sid in service_ids:
            svc = await self._services.get_by_id(sid)
            if svc is None or not svc.is_active:
                raise BusinessRuleError(message=f"Serviço {sid} indisponível.")
            total_dur += svc.total_duration
            total_price += svc.effective_price

        end_time_dt = datetime.combine(booking_date, start_time) + timedelta(minutes=total_dur)
        end_time = end_time_dt.time()

        # 3. Validar disponibilidade
        results = await self._availability.get_available_slots(
            tenant_id, professional_id, booking_date, booking_date, service_ids,
        )
        day_result = next((r for r in results if r.date == booking_date), None)
        if day_result is None or not any(
            s.start == start_time for s in day_result.slots
        ):
            raise BusinessRuleError(message="Horário indisponível.")

        # 4. Validar não ultrapassa max_advance_days
        max_adv = max(
            (await self._services.get_by_id(sid)).max_advance_days
            for sid in service_ids if await self._services.get_by_id(sid)
        ) if service_ids else 90
        if (booking_date - date.today()).days > max_adv:
            raise BusinessRuleError(message=f"Agendamento máximo com {max_adv} dias de antecedência.")

        # 5. Criar booking
        booking = Booking(
            id=str(uuid4()), tenant_id=tenant_id,
            professional_id=professional_id,
            booking_date=booking_date, start_time=start_time, end_time=end_time,
            status=BookingStatus.PENDING,
            customer_id=str(kwargs.get("customer_id", "")) if kwargs.get("customer_id") else None,
            guest_name=str(kwargs.get("guest_name", "")) if kwargs.get("guest_name") else None,
            guest_phone=str(kwargs.get("guest_phone", "")) if kwargs.get("guest_phone") else None,
            guest_email=str(kwargs.get("guest_email", "")) if kwargs.get("guest_email") else None,
            notes=str(kwargs.get("notes", "")) if kwargs.get("notes") else None,
            total_amount=total_price, total_duration_minutes=total_dur,
            source=str(kwargs.get("source", "website")),
            idempotency_key=idemp_key if idemp_key else None,
            created_by=actor_id, service_ids=service_ids,
        )

        created = await self._bookings.create(booking)

        # 6. Log de status
        await self._log_status(created.id, None, BookingStatus.PENDING, actor_id)

        return created

    async def get_booking(self, booking_id: str) -> Booking:
        b = await self._bookings.get_by_id(booking_id)
        if b is None:
            raise NotFoundError(message="Agendamento não encontrado.")
        return b

    async def list_bookings(
        self, tenant_id: str, *, date_from: date | None = None, date_to: date | None = None,
        professional_id: str | None = None, status: str | None = None,
        offset: int = 0, limit: int = 50,
    ) -> tuple[list[Booking], int]:
        return await self._bookings.list_for_tenant(
            tenant_id, date_from=date_from, date_to=date_to,
            professional_id=professional_id, status=status, offset=offset, limit=limit,
        )

    async def confirm_booking(self, booking_id: str, actor_id: str | None = None) -> Booking:
        b = await self.get_booking(booking_id)
        old_status = b.status
        b.confirm()
        await self._bookings.update_status(booking_id, BookingStatus.CONFIRMED)
        await self._log_status(booking_id, old_status, BookingStatus.CONFIRMED, actor_id)
        return b

    async def start_booking(self, booking_id: str, actor_id: str | None = None) -> Booking:
        """Check-in: inicia o atendimento."""
        b = await self.get_booking(booking_id)
        old_status = b.status
        b.start_service()
        await self._bookings.update_status(
            booking_id, BookingStatus.IN_PROGRESS,
            checked_in_at=datetime.now(timezone.utc),
        )
        await self._log_status(booking_id, old_status, BookingStatus.IN_PROGRESS, actor_id)
        return b

    async def complete_booking(self, booking_id: str, actor_id: str | None = None) -> Booking:
        """Check-out: finaliza o atendimento."""
        b = await self.get_booking(booking_id)
        old_status = b.status
        b.complete()
        await self._bookings.update_status(
            booking_id, BookingStatus.COMPLETED,
            completed_at=datetime.now(timezone.utc),
        )
        await self._log_status(booking_id, old_status, BookingStatus.COMPLETED, actor_id)
        return b

    async def cancel_booking(
        self, booking_id: str, reason: str, actor_id: str | None = None,
        notify_waitlist: bool = True,
    ) -> Booking:
        b = await self.get_booking(booking_id)
        old_status = b.status
        b.cancel(reason, actor_id)
        await self._bookings.update_status(
            booking_id, BookingStatus.CANCELLED,
            cancelled_at=datetime.now(timezone.utc),
            cancelled_by=actor_id, cancellation_reason=reason,
        )
        await self._log_status(booking_id, old_status, BookingStatus.CANCELLED, actor_id, reason)

        # Auto-promote waitlist
        if notify_waitlist:
            await self._promote_waitlist(b.tenant_id, b.professional_id, b.booking_date)

        return b

    async def mark_no_show(self, booking_id: str, actor_id: str | None = None) -> Booking:
        b = await self.get_booking(booking_id)
        old_status = b.status
        b.mark_no_show()
        await self._bookings.update_status(booking_id, BookingStatus.NO_SHOW)
        await self._log_status(booking_id, old_status, BookingStatus.NO_SHOW, actor_id)
        return b

    async def reschedule_booking(
        self, booking_id: str, new_date: date, new_start_time: str,
        new_professional_id: str | None = None, reason: str = "",
        actor_id: str | None = None,
    ) -> Booking:
        """Reagenda: marca o atual como RESCHEDULED e cria um novo."""
        old = await self.get_booking(booking_id)
        old_status = old.status

        # Criar novo booking
        prof_id = new_professional_id or old.professional_id

        # Extrair hora
        parts = new_start_time.split(":")
        start_t = time(int(parts[0]), int(parts[1]))
        end_dt = datetime.combine(new_date, start_t) + timedelta(minutes=old.total_duration_minutes)

        new_booking = Booking(
            id=str(uuid4()), tenant_id=old.tenant_id,
            professional_id=prof_id,
            booking_date=new_date, start_time=start_t, end_time=end_dt.time(),
            status=BookingStatus.PENDING,
            customer_id=old.customer_id,
            guest_name=old.guest_name, guest_phone=old.guest_phone,
            guest_email=old.guest_email,
            notes=old.notes, total_amount=old.total_amount,
            total_duration_minutes=old.total_duration_minutes,
            source=old.source, created_by=actor_id,
            service_ids=old.service_ids,
            rescheduled_from_id=booking_id,
        )

        created = await self._bookings.create(new_booking)

        # Marcar antigo como rescheduled
        old.reschedule_to(created.id)
        await self._bookings.update_status(
            booking_id, BookingStatus.RESCHEDULED,
            rescheduled_to_id=created.id,
        )
        await self._log_status(
            booking_id, old_status, BookingStatus.RESCHEDULED, actor_id,
            f"Reagendado para {new_date} {new_start_time}. {reason}",
        )
        await self._log_status(created.id, None, BookingStatus.PENDING, actor_id,
                               f"Reagendado de booking {booking_id}")

        # Promover waitlist para o slot liberado
        await self._promote_waitlist(old.tenant_id, old.professional_id, old.booking_date)

        return created

    async def get_booking_history(self, booking_id: str) -> list[BookingStatusLog]:
        return await self._logs.get_for_booking(booking_id)

    # ============================================================
    # Blocked Dates
    # ============================================================

    async def list_blocked_dates(
        self, tenant_id: str, *, date_from: date | None = None, date_to: date | None = None,
    ) -> list[BlockedDate]:
        return await self._blocked.get_for_tenant(tenant_id, date_from=date_from, date_to=date_to)

    async def create_blocked_date(self, tenant_id: str, actor_id: str | None, **kwargs: object) -> BlockedDate:
        bd = BlockedDate(
            id=str(uuid4()), tenant_id=tenant_id,
            blocked_date=kwargs["blocked_date"],
            professional_id=str(kwargs.get("professional_id", "")) if kwargs.get("professional_id") else None,
            block_type=str(kwargs.get("block_type", "full_day")),
            reason=str(kwargs.get("reason", "")),
            is_recurring=bool(kwargs.get("is_recurring", False)),
            recurring_pattern=str(kwargs.get("recurring_pattern", "")) if kwargs.get("recurring_pattern") else None,
            recurring_until=kwargs.get("recurring_until"),
            created_by=actor_id,
        )
        return await self._blocked.create(bd)

    async def delete_blocked_date(self, blocked_id: str) -> None:
        await self._blocked.delete(blocked_id)

    # ============================================================
    # Waitlist
    # ============================================================

    async def join_waitlist(self, tenant_id: str, **kwargs: object) -> WaitlistEntry:
        entry = WaitlistEntry(
            id=str(uuid4()), tenant_id=tenant_id,
            customer_id=str(kwargs.get("customer_id", "")) if kwargs.get("customer_id") else None,
            guest_name=str(kwargs.get("guest_name", "")) if kwargs.get("guest_name") else None,
            guest_phone=str(kwargs.get("guest_phone", "")) if kwargs.get("guest_phone") else None,
            professional_id=str(kwargs.get("professional_id", "")) if kwargs.get("professional_id") else None,
            service_id=str(kwargs.get("service_id", "")) if kwargs.get("service_id") else None,
            desired_date=kwargs.get("desired_date"),
            desired_period=str(kwargs.get("desired_period", "any")),
        )
        return await self._waitlist.create(entry)

    async def list_waitlist(self, tenant_id: str, *, status: str | None = None) -> list[WaitlistEntry]:
        return await self._waitlist.list_for_tenant(tenant_id, status=status)

    async def _promote_waitlist(self, tenant_id: str, professional_id: str, desired_date: date) -> None:
        """Auto-promotion: notifica próximo da fila quando slot libera."""
        next_entry = await self._waitlist.get_next_in_line(professional_id, desired_date)
        if next_entry:
            next_entry.notify(expires_hours=24)
            await self._waitlist.update_status(next_entry.id, WaitlistStatus.NOTIFIED)
            # TODO: Enviar notificação (WhatsApp/Email)

    # ============================================================
    # Helpers
    # ============================================================

    async def _log_status(
        self, booking_id: str, from_status: str | None,
        to_status: str, actor_id: str | None, notes: str | None = None,
    ) -> None:
        await self._logs.log(BookingStatusLog(
            id=str(uuid4()), booking_id=booking_id,
            from_status=from_status, to_status=to_status,
            changed_by=actor_id, notes=notes,
        ))
