"""Scheduling Module — Repository Implementation."""

from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import func, select, update, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.scheduling.domain.entities import (
    BlockedDate,
    Booking,
    BookingStatusLog,
    ProfessionalService,
    Service,
    ServiceCategory,
    WaitlistEntry,
)
from app.modules.scheduling.domain.interfaces import (
    IBlockedDateRepository,
    IBookingRepository,
    IBookingStatusLogRepository,
    IProfessionalServiceRepository,
    IServiceCategoryRepository,
    IServiceRepository,
    IWaitlistRepository,
)
from app.modules.scheduling.domain.value_objects import ServicePricing
from app.modules.scheduling.infrastructure.models.scheduling_models import (
    BlockedDateModel,
    BookingModel,
    BookingServiceModel,
    BookingStatusLogModel,
    ProfessionalServiceModel,
    ServiceCategoryModel,
    ServiceModel,
    WaitlistEntryModel,
)


# ============================================================
# Mappers
# ============================================================

def _svc_to_entity(m: ServiceModel) -> Service:
    return Service(
        id=m.id, tenant_id=m.tenant_id or "", name=m.name,
        category_id=m.category_id, description=m.description or "",
        duration_minutes=m.duration_minutes, buffer_minutes=m.buffer_minutes,
        pricing=ServicePricing(
            base_price=m.base_price, promotional_price=m.promotional_price,
            requires_deposit=m.requires_deposit, deposit_value=m.deposit_value,
        ),
        color_tag=m.color_tag, image_url=m.image_url,
        is_active=m.is_active, sort_order=m.sort_order,
        min_advance_minutes=m.min_advance_minutes,
        max_advance_days=m.max_advance_days,
        notes=m.notes, metadata=m.metadata or {},
        created_at=m.created_at, updated_at=m.updated_at, deleted_at=m.deleted_at,
    )


def _cat_to_entity(m: ServiceCategoryModel) -> ServiceCategory:
    return ServiceCategory(
        id=m.id, tenant_id=m.tenant_id or "", name=m.name,
        description=m.description or "", color_tag=m.color_tag,
        is_active=m.is_active, sort_order=m.sort_order, created_at=m.created_at,
    )


def _ps_to_entity(m: ProfessionalServiceModel) -> ProfessionalService:
    return ProfessionalService(
        id=m.id, tenant_id=m.tenant_id or "",
        professional_id=m.professional_id, service_id=m.service_id,
        custom_price=m.custom_price, custom_duration=m.custom_duration,
        is_active=m.is_active, created_at=m.created_at,
    )


def _booking_to_entity(m: BookingModel) -> Booking:
    svc_ids = [bs.service_id for bs in (m.booking_services or [])]
    return Booking(
        id=m.id, tenant_id=m.tenant_id or "", professional_id=m.professional_id,
        booking_date=m.booking_date, start_time=m.start_time, end_time=m.end_time,
        status=m.status, customer_id=m.customer_id,
        guest_name=m.guest_name, guest_phone=m.guest_phone, guest_email=m.guest_email,
        notes=m.notes, total_amount=m.total_amount,
        total_duration_minutes=m.total_duration_minutes,
        discount_amount=m.discount_amount, source=m.source,
        idempotency_key=m.idempotency_key, created_by=m.created_by,
        cancelled_at=m.cancelled_at, cancelled_by=m.cancelled_by,
        cancellation_reason=m.cancellation_reason,
        checked_in_at=m.checked_in_at, completed_at=m.completed_at,
        rescheduled_from_id=m.rescheduled_from_id,
        rescheduled_to_id=m.rescheduled_to_id,
        metadata=m.metadata or {}, service_ids=svc_ids,
        created_at=m.created_at, updated_at=m.updated_at,
    )


def _blocked_to_entity(m: BlockedDateModel) -> BlockedDate:
    return BlockedDate(
        id=m.id, tenant_id=m.tenant_id or "", blocked_date=m.blocked_date,
        professional_id=m.professional_id, block_type=m.block_type,
        reason=m.reason or "", start_time=m.start_time, end_time=m.end_time,
        is_recurring=m.is_recurring, recurring_pattern=m.recurring_pattern,
        recurring_until=m.recurring_until, created_by=m.created_by,
        created_at=m.created_at,
    )


# ============================================================
# ServiceRepository
# ============================================================

class ServiceRepository(IServiceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, service_id: str) -> Service | None:
        r = await self._s.execute(select(ServiceModel).where(ServiceModel.id == service_id))
        m = r.scalar_one_or_none()
        return _svc_to_entity(m) if m else None

    async def list_by_tenant(self, tenant_id: str, *, category_id: str | None = None, active_only: bool = True) -> list[Service]:
        stmt = select(ServiceModel).where(
            ServiceModel.tenant_id == tenant_id, ServiceModel.deleted_at.is_(None),
        )
        if active_only:
            stmt = stmt.where(ServiceModel.is_active.is_(True))
        if category_id:
            stmt = stmt.where(ServiceModel.category_id == category_id)
        r = await self._s.execute(stmt.order_by(ServiceModel.sort_order))
        return [_svc_to_entity(m) for m in r.scalars().all()]

    async def create(self, svc: Service) -> Service:
        m = ServiceModel(
            id=svc.id, tenant_id=svc.tenant_id, name=svc.name,
            category_id=svc.category_id, description=svc.description,
            duration_minutes=svc.duration_minutes, buffer_minutes=svc.buffer_minutes,
            base_price=svc.base_price, promotional_price=svc.pricing.promotional_price,
            color_tag=svc.color_tag, is_active=svc.is_active, sort_order=svc.sort_order,
            min_advance_minutes=svc.min_advance_minutes, max_advance_days=svc.max_advance_days,
            notes=svc.notes, metadata=svc.metadata,
        )
        self._s.add(m)
        await self._s.flush()
        return _svc_to_entity(m)

    async def update(self, svc: Service) -> Service:
        m = await self._s.get(ServiceModel, svc.id)
        if not m:
            raise ValueError(f"Service {svc.id} not found")
        for f in ("name", "description", "duration_minutes", "buffer_minutes",
                   "color_tag", "is_active", "sort_order", "notes", "category_id",
                   "min_advance_minutes", "max_advance_days", "metadata"):
            setattr(m, f, getattr(svc, f))
        m.base_price = svc.base_price
        m.promotional_price = svc.pricing.promotional_price
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _svc_to_entity(m)

    async def soft_delete(self, service_id: str) -> None:
        await self._s.execute(
            update(ServiceModel).where(ServiceModel.id == service_id)
            .values(deleted_at=datetime.now(timezone.utc))
        )


# ============================================================
# ServiceCategoryRepository
# ============================================================

class ServiceCategoryRepository(IServiceCategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def list_by_tenant(self, tenant_id: str) -> list[ServiceCategory]:
        r = await self._s.execute(
            select(ServiceCategoryModel)
            .where(ServiceCategoryModel.tenant_id == tenant_id)
            .order_by(ServiceCategoryModel.sort_order)
        )
        return [_cat_to_entity(m) for m in r.scalars().all()]

    async def create(self, cat: ServiceCategory) -> ServiceCategory:
        m = ServiceCategoryModel(
            id=cat.id, tenant_id=cat.tenant_id, name=cat.name,
            description=cat.description, color_tag=cat.color_tag, sort_order=cat.sort_order,
        )
        self._s.add(m)
        await self._s.flush()
        return _cat_to_entity(m)

    async def update(self, cat: ServiceCategory) -> ServiceCategory:
        m = await self._s.get(ServiceCategoryModel, cat.id)
        if not m:
            raise ValueError(f"Category {cat.id} not found")
        for f in ("name", "description", "color_tag", "is_active", "sort_order"):
            setattr(m, f, getattr(cat, f))
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _cat_to_entity(m)

    async def delete(self, category_id: str) -> None:
        await self._s.execute(sa_delete(ServiceCategoryModel).where(ServiceCategoryModel.id == category_id))


# ============================================================
# ProfessionalServiceRepository
# ============================================================

class ProfessionalServiceRepository(IProfessionalServiceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_services_for_professional(self, professional_id: str) -> list[ProfessionalService]:
        r = await self._s.execute(
            select(ProfessionalServiceModel)
            .where(ProfessionalServiceModel.professional_id == professional_id)
            .where(ProfessionalServiceModel.is_active.is_(True))
        )
        return [_ps_to_entity(m) for m in r.scalars().all()]

    async def get_professionals_for_service(self, service_id: str) -> list[ProfessionalService]:
        r = await self._s.execute(
            select(ProfessionalServiceModel)
            .where(ProfessionalServiceModel.service_id == service_id)
            .where(ProfessionalServiceModel.is_active.is_(True))
        )
        return [_ps_to_entity(m) for m in r.scalars().all()]

    async def upsert_batch(self, professional_id: str, services: list[ProfessionalService]) -> list[ProfessionalService]:
        await self._s.execute(
            sa_delete(ProfessionalServiceModel).where(ProfessionalServiceModel.professional_id == professional_id)
        )
        models = [
            ProfessionalServiceModel(
                id=ps.id, tenant_id=ps.tenant_id, professional_id=professional_id,
                service_id=ps.service_id, custom_price=ps.custom_price,
                custom_duration=ps.custom_duration, is_active=ps.is_active,
            )
            for ps in services
        ]
        self._s.add_all(models)
        await self._s.flush()
        return [_ps_to_entity(m) for m in models]

    async def remove(self, professional_service_id: str) -> None:
        await self._s.execute(sa_delete(ProfessionalServiceModel).where(ProfessionalServiceModel.id == professional_service_id))


# ============================================================
# BookingRepository
# ============================================================

class BookingRepository(IBookingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, booking_id: str) -> Booking | None:
        r = await self._s.execute(
            select(BookingModel).where(BookingModel.id == booking_id)
        )
        m = r.scalar_one_or_none()
        return _booking_to_entity(m) if m else None

    async def get_by_idempotency_key(self, key: str) -> Booking | None:
        r = await self._s.execute(
            select(BookingModel).where(BookingModel.idempotency_key == key)
        )
        m = r.scalar_one_or_none()
        return _booking_to_entity(m) if m else None

    async def create(self, booking: Booking) -> Booking:
        m = BookingModel(
            id=booking.id, tenant_id=booking.tenant_id, professional_id=booking.professional_id,
            booking_date=booking.booking_date, start_time=booking.start_time,
            end_time=booking.end_time, status=booking.status,
            customer_id=booking.customer_id,
            guest_name=booking.guest_name, guest_phone=booking.guest_phone,
            guest_email=booking.guest_email, notes=booking.notes,
            total_amount=booking.total_amount, total_duration_minutes=booking.total_duration_minutes,
            discount_amount=booking.discount_amount, source=booking.source,
            idempotency_key=booking.idempotency_key, created_by=booking.created_by,
            metadata=booking.metadata,
        )
        self._s.add(m)
        # Inserir booking_services
        for sid in booking.service_ids:
            self._s.add(BookingServiceModel(
                booking_id=booking.id, service_id=sid,
                service_name="", price=0, duration_minutes=0,
            ))
        await self._s.flush()
        return _booking_to_entity(m)

    async def update(self, booking: Booking) -> Booking:
        m = await self._s.get(BookingModel, booking.id)
        if not m:
            raise ValueError(f"Booking {booking.id} not found")
        for f in ("status", "notes", "total_amount", "discount_amount", "metadata"):
            setattr(m, f, getattr(booking, f))
        m.updated_at = datetime.now(timezone.utc)
        await self._s.flush()
        return _booking_to_entity(m)

    async def update_status(self, booking_id: str, status: str, **kwargs: object) -> None:
        vals: dict = {"status": status, "updated_at": datetime.now(timezone.utc)}
        for k, v in kwargs.items():
            if hasattr(BookingModel, k) and v is not None:
                vals[k] = v
        await self._s.execute(
            update(BookingModel).where(BookingModel.id == booking_id).values(**vals)
        )

    async def list_for_tenant(
        self, tenant_id: str, *, date_from: date | None = None, date_to: date | None = None,
        professional_id: str | None = None, status: str | None = None,
        offset: int = 0, limit: int = 50,
    ) -> tuple[list[Booking], int]:
        base = select(BookingModel).where(BookingModel.tenant_id == tenant_id)
        count_q = select(func.count()).select_from(BookingModel).where(BookingModel.tenant_id == tenant_id)
        if date_from:
            base = base.where(BookingModel.booking_date >= date_from)
            count_q = count_q.where(BookingModel.booking_date >= date_from)
        if date_to:
            base = base.where(BookingModel.booking_date <= date_to)
            count_q = count_q.where(BookingModel.booking_date <= date_to)
        if professional_id:
            base = base.where(BookingModel.professional_id == professional_id)
            count_q = count_q.where(BookingModel.professional_id == professional_id)
        if status:
            base = base.where(BookingModel.status == status)
            count_q = count_q.where(BookingModel.status == status)
        total = (await self._s.execute(count_q)).scalar() or 0
        r = await self._s.execute(
            base.order_by(BookingModel.booking_date, BookingModel.start_time).offset(offset).limit(limit)
        )
        return [_booking_to_entity(m) for m in r.scalars().all()], total

    async def list_for_professional(
        self, professional_id: str, *, date_from: date | None = None, date_to: date | None = None,
    ) -> list[Booking]:
        stmt = select(BookingModel).where(BookingModel.professional_id == professional_id)
        if date_from:
            stmt = stmt.where(BookingModel.booking_date >= date_from)
        if date_to:
            stmt = stmt.where(BookingModel.booking_date <= date_to)
        r = await self._s.execute(stmt.order_by(BookingModel.booking_date, BookingModel.start_time))
        return [_booking_to_entity(m) for m in r.scalars().all()]

    async def get_bookings_for_date_range(
        self, tenant_id: str, professional_id: str, start_date: date, end_date: date,
    ) -> list[Booking]:
        r = await self._s.execute(
            select(BookingModel).where(
                BookingModel.tenant_id == tenant_id,
                BookingModel.professional_id == professional_id,
                BookingModel.booking_date >= start_date,
                BookingModel.booking_date <= end_date,
                BookingModel.status.in_(["pending", "confirmed", "in_progress"]),
            )
        )
        return [_booking_to_entity(m) for m in r.scalars().all()]

    async def count_in_period(self, tenant_id: str, start_date: date, end_date: date) -> int:
        r = await self._s.execute(
            select(func.count()).select_from(BookingModel).where(
                BookingModel.tenant_id == tenant_id,
                BookingModel.booking_date >= start_date,
                BookingModel.booking_date <= end_date,
            )
        )
        return (r.scalar() or 0)


# ============================================================
# BookingStatusLogRepository
# ============================================================

class BookingStatusLogRepository(IBookingStatusLogRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def log(self, entry: BookingStatusLog) -> BookingStatusLog:
        m = BookingStatusLogModel(
            id=entry.id, booking_id=entry.booking_id,
            from_status=entry.from_status, to_status=entry.to_status,
            changed_by=entry.changed_by, ip_address=entry.ip_address,
            notes=entry.notes,
        )
        self._s.add(m)
        await self._s.flush()
        return entry

    async def get_for_booking(self, booking_id: str) -> list[BookingStatusLog]:
        r = await self._s.execute(
            select(BookingStatusLogModel)
            .where(BookingStatusLogModel.booking_id == booking_id)
            .order_by(BookingStatusLogModel.created_at)
        )
        return [
            BookingStatusLog(
                id=m.id, booking_id=m.booking_id,
                from_status=m.from_status, to_status=m.to_status,
                changed_by=m.changed_by, ip_address=m.ip_address,
                notes=m.notes, created_at=m.created_at,
            )
            for m in r.scalars().all()
        ]


# ============================================================
# BlockedDateRepository
# ============================================================

class BlockedDateRepository(IBlockedDateRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_for_tenant(self, tenant_id: str, *, date_from: date | None = None, date_to: date | None = None) -> list[BlockedDate]:
        stmt = select(BlockedDateModel).where(BlockedDateModel.tenant_id == tenant_id)
        if date_from:
            stmt = stmt.where(BlockedDateModel.blocked_date >= date_from)
        if date_to:
            stmt = stmt.where(BlockedDateModel.blocked_date <= date_to)
        r = await self._s.execute(stmt.order_by(BlockedDateModel.blocked_date))
        return [_blocked_to_entity(m) for m in r.scalars().all()]

    async def get_for_professional(self, professional_id: str, date_from: date, date_to: date) -> list[BlockedDate]:
        r = await self._s.execute(
            select(BlockedDateModel).where(
                BlockedDateModel.blocked_date >= date_from,
                BlockedDateModel.blocked_date <= date_to,
                (BlockedDateModel.professional_id == professional_id) |
                (BlockedDateModel.professional_id.is_(None)),
            )
        )
        return [_blocked_to_entity(m) for m in r.scalars().all()]

    async def create(self, blocked: BlockedDate) -> BlockedDate:
        m = BlockedDateModel(
            id=blocked.id, tenant_id=blocked.tenant_id, blocked_date=blocked.blocked_date,
            professional_id=blocked.professional_id, block_type=blocked.block_type,
            reason=blocked.reason, start_time=blocked.start_time, end_time=blocked.end_time,
            is_recurring=blocked.is_recurring, recurring_pattern=blocked.recurring_pattern,
            recurring_until=blocked.recurring_until, created_by=blocked.created_by,
        )
        self._s.add(m)
        await self._s.flush()
        return _blocked_to_entity(m)

    async def delete(self, blocked_id: str) -> None:
        await self._s.execute(sa_delete(BlockedDateModel).where(BlockedDateModel.id == blocked_id))

    async def is_date_blocked(self, tenant_id: str, professional_id: str | None, check_date: date) -> bool:
        r = await self._s.execute(
            select(func.count()).select_from(BlockedDateModel).where(
                BlockedDateModel.tenant_id == tenant_id,
                BlockedDateModel.blocked_date == check_date,
                (BlockedDateModel.professional_id == professional_id) |
                (BlockedDateModel.professional_id.is_(None)),
            )
        )
        return (r.scalar() or 0) > 0


# ============================================================
# WaitlistRepository
# ============================================================

class WaitlistRepository(IWaitlistRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_id(self, entry_id: str) -> WaitlistEntry | None:
        r = await self._s.execute(select(WaitlistEntryModel).where(WaitlistEntryModel.id == entry_id))
        m = r.scalar_one_or_none()
        if not m:
            return None
        return WaitlistEntry(
            id=m.id, tenant_id=m.tenant_id or "", customer_id=m.customer_id,
            guest_name=m.guest_name, guest_phone=m.guest_phone,
            professional_id=m.professional_id, service_id=m.service_id,
            desired_date=m.desired_date, desired_period=m.desired_period,
            status=m.status, position=m.position,
            notified_at=m.notified_at, expires_at=m.expires_at, created_at=m.created_at,
        )

    async def create(self, entry: WaitlistEntry) -> WaitlistEntry:
        m = WaitlistEntryModel(
            id=entry.id, tenant_id=entry.tenant_id,
            customer_id=entry.customer_id, guest_name=entry.guest_name,
            guest_phone=entry.guest_phone, professional_id=entry.professional_id,
            service_id=entry.service_id, desired_date=entry.desired_date,
            desired_period=entry.desired_period, position=entry.position,
        )
        self._s.add(m)
        await self._s.flush()
        return entry

    async def update_status(self, entry_id: str, status: str) -> None:
        await self._s.execute(
            update(WaitlistEntryModel).where(WaitlistEntryModel.id == entry_id).values(status=status)
        )

    async def get_next_in_line(self, professional_id: str, desired_date: date) -> WaitlistEntry | None:
        r = await self._s.execute(
            select(WaitlistEntryModel)
            .where(WaitlistEntryModel.professional_id == professional_id)
            .where(WaitlistEntryModel.desired_date == desired_date)
            .where(WaitlistEntryModel.status == "waiting")
            .order_by(WaitlistEntryModel.position)
            .limit(1)
        )
        m = r.scalar_one_or_none()
        if not m:
            return None
        return WaitlistEntry(
            id=m.id, tenant_id=m.tenant_id or "", customer_id=m.customer_id,
            guest_name=m.guest_name, guest_phone=m.guest_phone,
            professional_id=m.professional_id, service_id=m.service_id,
            desired_date=m.desired_date, desired_period=m.desired_period,
            status=m.status, position=m.position,
            notified_at=m.notified_at, expires_at=m.expires_at, created_at=m.created_at,
        )

    async def list_for_tenant(self, tenant_id: str, *, status: str | None = None) -> list[WaitlistEntry]:
        stmt = select(WaitlistEntryModel).where(WaitlistEntryModel.tenant_id == tenant_id)
        if status:
            stmt = stmt.where(WaitlistEntryModel.status == status)
        r = await self._s.execute(stmt.order_by(WaitlistEntryModel.created_at))
        return [
            WaitlistEntry(
                id=m.id, tenant_id=m.tenant_id or "", customer_id=m.customer_id,
                guest_name=m.guest_name, guest_phone=m.guest_phone,
                professional_id=m.professional_id, service_id=m.service_id,
                desired_date=m.desired_date, desired_period=m.desired_period,
                status=m.status, position=m.position,
                notified_at=m.notified_at, expires_at=m.expires_at, created_at=m.created_at,
            )
            for m in r.scalars().all()
        ]
