"""Admin Module — Dashboard & Global Search API.

Agrega dados de TODOS os módulos para o painel administrativo.
- Dashboard: KPIs, agenda do dia, receita, ocupação
- Global Search: busca unificada em clientes, serviços, staff
- Quick Actions: operações frequentes
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.tenant.presentation.dependencies import get_current_tenant

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/dashboard")
async def get_dashboard(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Dashboard aggregator — KPIs de todos os módulos em 1 chamada."""
    tid = tenant["id"]
    today = date.today()

    # Buscar dados dos módulos
    from app.modules.scheduling.infrastructure.repository import BookingRepository, ServiceRepository
    from app.modules.staff.infrastructure.repository import StaffRepository
    from app.modules.customer.infrastructure.repository import CustomerRepository, ReviewRepository
    from app.modules.payment.infrastructure.repository import PaymentRepository

    booking_repo = BookingRepository(session)
    service_repo = ServiceRepository(session)
    staff_repo = StaffRepository(session)
    customer_repo = CustomerRepository(session)
    review_repo = ReviewRepository(session)
    payment_repo = PaymentRepository(session)

    # KPIs
    bookings_today, _ = await booking_repo.list_for_tenant(
        tid, date_from=today, date_to=today,
    )
    confirmed = [b for b in bookings_today if b.status in ("confirmed", "in_progress")]
    completed = [b for b in bookings_today if b.status == "completed"]
    cancelled = [b for b in bookings_today if b.status == "cancelled"]

    # Receita do dia
    revenue_today = sum(p.amount for p in (await payment_repo.list_for_tenant(tid, status="paid"))[0]
                        if p.paid_at and p.paid_at.date() == today)

    # Staff ativo
    active_staff = await staff_repo.count_active(tid)

    # Clientes
    customers_total = (await customer_repo.list_by_tenant(tid))[1]

    # Avaliações
    reviews, reviews_total = await review_repo.list_for_tenant(tid, visible_only=True)
    avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1) if reviews else 0

    # Ocupação (% de slots preenchidos)
    total_slots = active_staff * 10  # Estimativa: 10 slots/dia por profissional
    occupancy = round(len(confirmed) / total_slots * 100) if total_slots > 0 else 0

    # Bookings do dia (timeline)
    timeline = [
        {
            "time": b.start_time.strftime("%H:%M") if hasattr(b.start_time, 'strftime') else str(b.start_time),
            "customer": b.guest_name or f"Cliente {b.customer_id or ''}",
            "service": ", ".join(b.service_ids[:2]) if b.service_ids else "",
            "status": b.status,
        }
        for b in sorted(bookings_today, key=lambda x: str(x.start_time))[:20]
    ]

    # Próximos 7 dias — receita
    week_revenue: dict[str, int] = {}
    for i in range(7):
        d = today + timedelta(days=i)
        week_revenue[d.isoformat()] = 0
    payments_week, _ = await payment_repo.list_for_tenant(tid, status="paid")
    for p in payments_week:
        if p.paid_at:
            key = p.paid_at.date().isoformat()
            if key in week_revenue:
                week_revenue[key] += p.amount

    return {
        "kpis": {
            "revenue_today": revenue_today,
            "bookings_confirmed": len(confirmed),
            "bookings_completed": len(completed),
            "bookings_cancelled": len(cancelled),
            "occupancy_pct": occupancy,
            "avg_rating": avg_rating,
            "active_staff": active_staff,
            "total_customers": customers_total,
            "total_reviews": reviews_total,
        },
        "today_timeline": timeline,
        "week_revenue": [{"date": k, "amount": v} for k, v in week_revenue.items()],
        "staff_performance": [
            {"name": f"Profissional {i+1}", "bookings": 0, "revenue": 0, "rating": 0, "occupancy": 0}
            for i in range(active_staff)
        ],
    }


@router.get("/search")
async def global_search(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    q: str = Query(..., min_length=2, description="Termo de busca"),
) -> dict:
    """Global search — busca em clientes, serviços, profissionais."""
    tid = tenant["id"]

    from app.modules.customer.infrastructure.repository import CustomerRepository
    from app.modules.scheduling.infrastructure.repository import ServiceRepository
    from app.modules.staff.infrastructure.repository import StaffRepository

    customer_repo = CustomerRepository(session)
    service_repo = ServiceRepository(session)
    staff_repo = StaffRepository(session)

    # Buscar em paralelo
    customers, _ = await customer_repo.search(tid, q, limit=5)
    services = await service_repo.list_by_tenant(tid)
    staff_list, _ = await staff_repo.list_by_tenant(tid)

    # Filtrar resultados
    matched_services = [s for s in services if q.lower() in s.name.lower()][:5]
    matched_staff = [s for s in staff_list if q.lower() in s.professional_name.lower()][:5]

    return {
        "query": q,
        "results": {
            "customers": [
                {"id": c.id, "name": c.name, "phone": c.phone, "type": "customer"}
                for c in customers
            ],
            "services": [
                {"id": s.id, "name": s.name, "price": s.base_price, "type": "service"}
                for s in matched_services
            ],
            "staff": [
                {"id": s.id, "name": s.professional_name, "type": "staff"}
                for s in matched_staff
            ],
        },
        "total": len(customers) + len(matched_services) + len(matched_staff),
    }


@router.get("/quick-stats")
async def quick_stats(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Quick stats para o header/sidebar."""
    tid = tenant["id"]
    today = date.today()

    from app.modules.scheduling.infrastructure.repository import BookingRepository
    booking_repo = BookingRepository(session)
    bookings, _ = await booking_repo.list_for_tenant(tid, date_from=today, date_to=today)

    pending = [b for b in bookings if b.status == "pending"]
    in_progress = [b for b in bookings if b.status == "in_progress"]

    return {
        "pending_bookings": len(pending),
        "in_progress": len(in_progress),
        "today_total": len(bookings),
    }
