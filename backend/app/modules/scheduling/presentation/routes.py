"""Scheduling Module — API Routes.

Endpoints REST para:
- Serviços e Categorias
- Disponibilidade (availability engine)
- Agendamentos (CRUD, state machine, reschedule, cancel)
- Bloqueios
- Lista de Espera
- Smart Suggestions
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.scheduling.application.dto import (
    BlockedDateCreateRequest,
    BlockedDateResponse,
    BookingCancelRequest,
    BookingCreateRequest,
    BookingListResponse,
    BookingRescheduleRequest,
    BookingResponse,
    CategoryCreateRequest,
    CategoryResponse,
    ProfessionalServiceBatchRequest,
    ServiceCreateRequest,
    ServiceResponse,
    ServiceUpdateRequest,
    SmartSuggestionResponse,
    WaitlistCreateRequest,
    WaitlistResponse,
)
from app.modules.scheduling.application.scheduling_service import SchedulingService
from app.modules.scheduling.infrastructure.availability_engine import AvailabilityEngine
from app.modules.scheduling.infrastructure.repository import (
    BlockedDateRepository,
    BookingRepository,
    BookingStatusLogRepository,
    ProfessionalServiceRepository,
    ServiceCategoryRepository,
    ServiceRepository,
    WaitlistRepository,
)
from app.modules.tenant.presentation.dependencies import get_current_tenant

router = APIRouter(prefix="/scheduling", tags=["Scheduling"])


def _get_service(session: AsyncSession) -> SchedulingService:
    return SchedulingService(
        service_repo=ServiceRepository(session),
        category_repo=ServiceCategoryRepository(session),
        prof_svc_repo=ProfessionalServiceRepository(session),
        booking_repo=BookingRepository(session),
        status_log_repo=BookingStatusLogRepository(session),
        blocked_repo=BlockedDateRepository(session),
        waitlist_repo=WaitlistRepository(session),
        availability=AvailabilityEngine(session),
    )


def _actor(request: Request) -> str | None:
    return getattr(request.state, "user_id", None)


# ============================================================
# CATEGORIES
# ============================================================

@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[CategoryResponse]:
    svc = _get_service(session)
    cats = await svc.list_categories(tenant["id"])
    return [CategoryResponse(**c.__dict__) for c in cats]


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    body: CategoryCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> CategoryResponse:
    svc = _get_service(session)
    c = await svc.create_category(tenant["id"], **body.model_dump())
    return CategoryResponse(**c.__dict__)


# ============================================================
# SERVICES
# ============================================================

@router.get("/services", response_model=list[ServiceResponse])
async def list_services(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    category_id: str | None = Query(default=None),
) -> list[ServiceResponse]:
    svc = _get_service(session)
    services = await svc.list_services(tenant["id"], category_id=category_id)
    return [_svc_response(s) for s in services]


@router.get("/services/{service_id}", response_model=ServiceResponse)
async def get_service(
    service_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> ServiceResponse:
    svc = _get_service(session)
    s = await svc.get_service(service_id)
    return _svc_response(s)


@router.post("/services", response_model=ServiceResponse, status_code=201)
async def create_service(
    body: ServiceCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> ServiceResponse:
    svc = _get_service(session)
    s = await svc.create_service(tenant["id"], **body.model_dump())
    return _svc_response(s)


@router.patch("/services/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: str,
    body: ServiceUpdateRequest,
    session: AsyncSession = Depends(get_async_session),
) -> ServiceResponse:
    svc = _get_service(session)
    s = await svc.update_service(service_id, **body.model_dump(exclude_none=True))
    return _svc_response(s)


@router.delete("/services/{service_id}")
async def delete_service(
    service_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.delete_service(service_id)
    return {"message": "Serviço removido."}


# ============================================================
# PROFESSIONAL SERVICES
# ============================================================

@router.get("/professionals/{professional_id}/services")
async def get_professional_services(
    professional_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _get_service(session)
    links = await svc.get_professional_services(professional_id)
    return [{"service_id": l.service_id, "custom_price": l.custom_price, "custom_duration": l.custom_duration} for l in links]


@router.put("/professionals/{professional_id}/services")
async def link_professional_services(
    professional_id: str,
    body: ProfessionalServiceBatchRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _get_service(session)
    links = await svc.link_professional_services(
        tenant["id"], professional_id, [s.model_dump() for s in body.services],
    )
    return [{"id": l.id, "service_id": l.service_id} for l in links]


# ============================================================
# AVAILABILITY
# ============================================================

@router.get("/availability/{professional_id}")
async def get_availability(
    professional_id: str,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    date_from: date = Query(...),
    date_to: date = Query(...),
    service_ids: str = Query(..., description="Comma-separated service IDs"),
) -> list[dict]:
    svc = _get_service(session)
    ids = [s.strip() for s in service_ids.split(",") if s.strip()]
    return await svc.get_availability(tenant["id"], professional_id, date_from, date_to, ids)


@router.get("/suggestions", response_model=list[SmartSuggestionResponse])
async def get_smart_suggestions(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    service_ids: str = Query(..., description="Comma-separated service IDs"),
    professional_id: str | None = Query(default=None),
    from_date: date | None = Query(default=None),
    max_suggestions: int = Query(default=5, ge=1, le=20),
) -> list[SmartSuggestionResponse]:
    svc = _get_service(session)
    ids = [s.strip() for s in service_ids.split(",") if s.strip()]
    suggestions = await svc.get_smart_suggestions(
        tenant["id"], professional_id, ids, from_date=from_date, max_suggestions=max_suggestions,
    )
    return [SmartSuggestionResponse(**s) for s in suggestions]


# ============================================================
# BOOKINGS
# ============================================================

@router.get("/bookings", response_model=BookingListResponse)
async def list_bookings(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    professional_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> BookingListResponse:
    svc = _get_service(session)
    items, total = await svc.list_bookings(
        tenant["id"], date_from=date_from, date_to=date_to,
        professional_id=professional_id, status=status, offset=offset, limit=limit,
    )
    return BookingListResponse(
        items=[_booking_response(b) for b in items],
        total=total, offset=offset, limit=limit,
    )


@router.get("/bookings/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> BookingResponse:
    svc = _get_service(session)
    b = await svc.get_booking(booking_id)
    return _booking_response(b)


@router.post("/bookings", response_model=BookingResponse, status_code=201)
async def create_booking(
    body: BookingCreateRequest,
    request: Request,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> BookingResponse:
    svc = _get_service(session)
    b = await svc.create_booking(tenant["id"], _actor(request), **body.model_dump())
    return _booking_response(b)


@router.post("/bookings/{booking_id}/confirm", response_model=BookingResponse)
async def confirm_booking(
    booking_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> BookingResponse:
    svc = _get_service(session)
    b = await svc.confirm_booking(booking_id, _actor(request))
    return _booking_response(b)


@router.post("/bookings/{booking_id}/check-in", response_model=BookingResponse)
async def check_in(
    booking_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> BookingResponse:
    svc = _get_service(session)
    b = await svc.start_booking(booking_id, _actor(request))
    return _booking_response(b)


@router.post("/bookings/{booking_id}/check-out", response_model=BookingResponse)
async def check_out(
    booking_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> BookingResponse:
    svc = _get_service(session)
    b = await svc.complete_booking(booking_id, _actor(request))
    return _booking_response(b)


@router.post("/bookings/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    booking_id: str,
    body: BookingCancelRequest,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> BookingResponse:
    svc = _get_service(session)
    b = await svc.cancel_booking(booking_id, body.reason, _actor(request), body.notify_waitlist)
    return _booking_response(b)


@router.post("/bookings/{booking_id}/no-show", response_model=BookingResponse)
async def mark_no_show(
    booking_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> BookingResponse:
    svc = _get_service(session)
    b = await svc.mark_no_show(booking_id, _actor(request))
    return _booking_response(b)


@router.post("/bookings/{booking_id}/reschedule", response_model=BookingResponse, status_code=201)
async def reschedule_booking(
    booking_id: str,
    body: BookingRescheduleRequest,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> BookingResponse:
    svc = _get_service(session)
    b = await svc.reschedule_booking(
        booking_id, body.new_date, body.new_start_time,
        body.professional_id, body.reason, _actor(request),
    )
    return _booking_response(b)


@router.get("/bookings/{booking_id}/history")
async def get_booking_history(
    booking_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _get_service(session)
    logs = await svc.get_booking_history(booking_id)
    return [
        {"from_status": l.from_status, "to_status": l.to_status,
         "changed_by": l.changed_by, "notes": l.notes,
         "created_at": l.created_at.isoformat() if l.created_at else None}
        for l in logs
    ]


# ============================================================
# BLOCKED DATES
# ============================================================

@router.get("/blocked-dates", response_model=list[BlockedDateResponse])
async def list_blocked_dates(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> list[BlockedDateResponse]:
    svc = _get_service(session)
    items = await svc.list_blocked_dates(tenant["id"], date_from=date_from, date_to=date_to)
    return [BlockedDateResponse(**b.__dict__) for b in items]


@router.post("/blocked-dates", response_model=BlockedDateResponse, status_code=201)
async def create_blocked_date(
    body: BlockedDateCreateRequest,
    request: Request,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> BlockedDateResponse:
    svc = _get_service(session)
    b = await svc.create_blocked_date(tenant["id"], _actor(request), **body.model_dump())
    return BlockedDateResponse(**b.__dict__)


@router.delete("/blocked-dates/{blocked_id}")
async def delete_blocked_date(
    blocked_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.delete_blocked_date(blocked_id)
    return {"message": "Bloqueio removido."}


# ============================================================
# WAITLIST
# ============================================================

@router.get("/waitlist", response_model=list[WaitlistResponse])
async def list_waitlist(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    status: str | None = Query(default=None),
) -> list[WaitlistResponse]:
    svc = _get_service(session)
    items = await svc.list_waitlist(tenant["id"], status=status)
    return [WaitlistResponse(**w.__dict__) for w in items]


@router.post("/waitlist", response_model=WaitlistResponse, status_code=201)
async def join_waitlist(
    body: WaitlistCreateRequest,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> WaitlistResponse:
    svc = _get_service(session)
    w = await svc.join_waitlist(tenant["id"], **body.model_dump())
    return WaitlistResponse(**w.__dict__)


# ============================================================
# Response helpers
# ============================================================

def _svc_response(s: object) -> ServiceResponse:
    return ServiceResponse(
        id=getattr(s, "id", ""),
        name=getattr(s, "name", ""),
        category_id=getattr(s, "category_id", None),
        description=getattr(s, "description", ""),
        duration_minutes=getattr(s, "duration_minutes", 0),
        buffer_minutes=getattr(s, "buffer_minutes", 0),
        base_price=getattr(s, "base_price", 0),
        promotional_price=getattr(s, "promotional_price", 0),
        effective_price=getattr(s, "effective_price", 0),
        total_duration=getattr(s, "total_duration", 0),
        color_tag=getattr(s, "color_tag", ""),
        image_url=getattr(s, "image_url", None),
        is_active=getattr(s, "is_active", True),
        sort_order=getattr(s, "sort_order", 0),
        notes=getattr(s, "notes", None),
    )


def _booking_response(b: object) -> BookingResponse:
    return BookingResponse(
        id=getattr(b, "id", ""),
        professional_id=getattr(b, "professional_id", ""),
        booking_date=getattr(b, "booking_date", date.today()),
        start_time=getattr(b, "start_time", "00:00").strftime("%H:%M") if hasattr(getattr(b, "start_time", "00:00"), "strftime") else str(getattr(b, "start_time", "00:00")),
        end_time=getattr(b, "end_time", "00:00").strftime("%H:%M") if hasattr(getattr(b, "end_time", "00:00"), "strftime") else str(getattr(b, "end_time", "00:00")),
        status=getattr(b, "status", ""),
        customer_id=getattr(b, "customer_id", None),
        guest_name=getattr(b, "guest_name", None),
        guest_phone=getattr(b, "guest_phone", None),
        notes=getattr(b, "notes", None),
        total_amount=getattr(b, "total_amount", 0),
        total_duration_minutes=getattr(b, "total_duration_minutes", 0),
        discount_amount=getattr(b, "discount_amount", 0),
        source=getattr(b, "source", "website"),
        checked_in_at=getattr(b, "checked_in_at", None),
        completed_at=getattr(b, "completed_at", None),
        cancelled_at=getattr(b, "cancelled_at", None),
        cancellation_reason=getattr(b, "cancellation_reason", None),
        service_ids=getattr(b, "service_ids", []),
        created_at=getattr(b, "created_at", None),
    )
