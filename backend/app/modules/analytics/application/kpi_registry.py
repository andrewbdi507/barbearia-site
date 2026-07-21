"""Analytics Module — KPI Registry.

Registro modular de KPIs. Para adicionar novo KPI:
1. Criar função async que retorna KPIData
2. Registrar no KPI_REGISTRY

O dashboard auto-descobre todos os KPIs registrados.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import Any, Callable, Coroutine

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.domain.entities import KPIData


# KPI compute function signature
KPIComputeFn = Callable[[AsyncSession, str, date, date], Coroutine[Any, Any, KPIData]]


# ============================================================
# KPI Registry
# ============================================================

KPI_REGISTRY: dict[str, dict[str, Any]] = {}


def register_kpi(
    key: str, label: str, format: str, compute: KPIComputeFn,
    description: str = "",
) -> None:
    """Registra um KPI no dashboard."""
    KPI_REGISTRY[key] = {
        "key": key, "label": label, "format": format,
        "compute": compute, "description": description,
    }


# ============================================================
# Individual KPI Functions
# ============================================================

async def _kpi_revenue_today(session: AsyncSession, tid: str, dfrom: date, dto: date) -> KPIData:
    from app.modules.payment.infrastructure.models.payment_models import PaymentModel
    r = await session.execute(
        select(func.coalesce(func.sum(PaymentModel.amount), 0))
        .where(PaymentModel.tenant_id == tid)
        .where(PaymentModel.status == "paid")
        .where(func.date(PaymentModel.paid_at) == date.today())
    )
    val = r.scalar() or 0
    # Comparison: yesterday
    r2 = await session.execute(
        select(func.coalesce(func.sum(PaymentModel.amount), 0))
        .where(PaymentModel.tenant_id == tid)
        .where(PaymentModel.status == "paid")
        .where(func.date(PaymentModel.paid_at) == date.today() - timedelta(days=1))
    )
    yesterday = r2.scalar() or 0
    change = ((val - yesterday) / yesterday * 100) if yesterday > 0 else 0
    return KPIData(key="revenue_today", label="Receita Hoje", value=val, format="currency",
                   trend="up" if change > 0 else "down" if change < 0 else "stable",
                   change_pct=round(change, 1), vs_last_period=yesterday)


async def _kpi_bookings_today(session: AsyncSession, tid: str, dfrom: date, dto: date) -> KPIData:
    from app.modules.scheduling.infrastructure.models.scheduling_models import BookingModel
    r = await session.execute(
        select(func.count()).select_from(BookingModel)
        .where(BookingModel.tenant_id == tid)
        .where(BookingModel.booking_date == date.today())
        .where(BookingModel.status.in_(["confirmed", "completed", "in_progress"]))
    )
    return KPIData(key="bookings_today", label="Agendamentos Hoje", value=r.scalar() or 0,
                   format="number")


async def _kpi_cancellation_rate(session: AsyncSession, tid: str, dfrom: date, dto: date) -> KPIData:
    from app.modules.scheduling.infrastructure.models.scheduling_models import BookingModel
    total_r = await session.execute(
        select(func.count()).select_from(BookingModel)
        .where(BookingModel.tenant_id == tid)
        .where(BookingModel.booking_date >= dfrom).where(BookingModel.booking_date <= dto)
    )
    cancelled_r = await session.execute(
        select(func.count()).select_from(BookingModel)
        .where(BookingModel.tenant_id == tid)
        .where(BookingModel.booking_date >= dfrom).where(BookingModel.booking_date <= dto)
        .where(BookingModel.status == "cancelled")
    )
    total = total_r.scalar() or 1
    cancelled = cancelled_r.scalar() or 0
    rate = round(cancelled / total * 100, 1)
    return KPIData(key="cancellation_rate", label="Taxa de Cancelamento", value=rate,
                   format="percentage", trend="up" if rate > 20 else "stable")


async def _kpi_avg_ticket(session: AsyncSession, tid: str, dfrom: date, dto: date) -> KPIData:
    from app.modules.payment.infrastructure.models.payment_models import PaymentModel
    r = await session.execute(
        select(func.coalesce(func.avg(PaymentModel.amount), 0))
        .where(PaymentModel.tenant_id == tid)
        .where(PaymentModel.status == "paid")
        .where(func.date(PaymentModel.paid_at) >= dfrom)
        .where(func.date(PaymentModel.paid_at) <= dto)
    )
    return KPIData(key="avg_ticket", label="Ticket Médio", value=round(r.scalar() or 0),
                   format="currency")


async def _kpi_new_customers(session: AsyncSession, tid: str, dfrom: date, dto: date) -> KPIData:
    from app.modules.customer.infrastructure.models.customer_models import CustomerModel
    r = await session.execute(
        select(func.count()).select_from(CustomerModel)
        .where(CustomerModel.tenant_id == tid)
        .where(CustomerModel.deleted_at.is_(None))
        .where(func.date(CustomerModel.created_at) >= dfrom)
        .where(func.date(CustomerModel.created_at) <= dto)
    )
    return KPIData(key="new_customers", label="Novos Clientes", value=r.scalar() or 0, format="number")


async def _kpi_occupancy(session: AsyncSession, tid: str, dfrom: date, dto: date) -> KPIData:
    from app.modules.scheduling.infrastructure.models.scheduling_models import BookingModel
    from app.modules.staff.infrastructure.models.staff_models import StaffProfileModel
    staff_r = await session.execute(
        select(func.count()).select_from(StaffProfileModel)
        .where(StaffProfileModel.tenant_id == tid).where(StaffProfileModel.status == "active")
    )
    staff = staff_r.scalar() or 1
    bookings_r = await session.execute(
        select(func.count()).select_from(BookingModel)
        .where(BookingModel.tenant_id == tid)
        .where(BookingModel.booking_date >= dfrom).where(BookingModel.booking_date <= dto)
        .where(BookingModel.status.in_(["confirmed", "completed", "in_progress"]))
    )
    bookings = bookings_r.scalar() or 0
    max_slots = staff * 10 * ((dto - dfrom).days or 1)
    rate = round(bookings / max_slots * 100, 1)
    return KPIData(key="occupancy", label="Taxa de Ocupação", value=rate, format="percentage")


async def _kpi_no_show(session: AsyncSession, tid: str, dfrom: date, dto: date) -> KPIData:
    from app.modules.scheduling.infrastructure.models.scheduling_models import BookingModel
    r = await session.execute(
        select(func.count()).select_from(BookingModel)
        .where(BookingModel.tenant_id == tid)
        .where(BookingModel.booking_date >= dfrom).where(BookingModel.booking_date <= dto)
        .where(BookingModel.status == "no_show")
    )
    return KPIData(key="no_show", label="No-Show", value=r.scalar() or 0, format="number")


# ============================================================
# Register All KPIs
# ============================================================

def register_all_kpis() -> None:
    register_kpi("revenue_today", "Receita Hoje", "currency", _kpi_revenue_today)
    register_kpi("bookings_today", "Agendamentos Hoje", "number", _kpi_bookings_today)
    register_kpi("cancellation_rate", "Taxa de Cancelamento", "percentage", _kpi_cancellation_rate)
    register_kpi("avg_ticket", "Ticket Médio", "currency", _kpi_avg_ticket)
    register_kpi("new_customers", "Novos Clientes", "number", _kpi_new_customers)
    register_kpi("occupancy", "Taxa de Ocupação", "percentage", _kpi_occupancy)
    register_kpi("no_show", "No-Show", "number", _kpi_no_show)
