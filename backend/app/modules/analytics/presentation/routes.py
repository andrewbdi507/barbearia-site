"""Analytics Module — API Routes."""

from __future__ import annotations

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.modules.analytics.application.analytics_service import AnalyticsService
from app.modules.tenant.presentation.dependencies import get_current_tenant

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def _get_service(session: AsyncSession) -> AnalyticsService:
    return AnalyticsService(session)


# ============================================================
# KPIs
# ============================================================

@router.get("/kpis")
async def get_kpis(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    period: str = Query(default="today", pattern=r"^(today|yesterday|week|month|year)$"),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> list[dict]:
    svc = _get_service(session)
    kpis = await svc.compute_kpis(tenant["id"], period=period, date_from=date_from, date_to=date_to)
    return [k.__dict__ for k in kpis]


@router.get("/kpis/list")
async def list_available_kpis(
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _get_service(session)
    return await svc.get_kpi_list()


# ============================================================
# Charts
# ============================================================

@router.get("/charts/revenue")
async def revenue_chart(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    period: str = Query(default="week"),
) -> dict:
    svc = _get_service(session)
    chart = await svc.revenue_chart(tenant["id"], period)
    return chart.__dict__


@router.get("/charts/top-services")
async def top_services(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    limit: int = Query(default=5, ge=1, le=20),
) -> dict:
    svc = _get_service(session)
    chart = await svc.top_services(tenant["id"], limit)
    return chart.__dict__


@router.get("/charts/top-professionals")
async def top_professionals(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    limit: int = Query(default=5, ge=1, le=20),
) -> dict:
    svc = _get_service(session)
    chart = await svc.top_professionals(tenant["id"], limit)
    return chart.__dict__


@router.get("/charts/peak-hours")
async def peak_hours(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    chart = await svc.peak_hours(tenant["id"])
    return chart.__dict__


# ============================================================
# Goals
# ============================================================

@router.get("/goals")
async def list_goals(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _get_service(session)
    goals = await svc.list_goals(tenant["id"])
    return [{"id": g.id, "name": g.name, "metric": g.metric,
             "target": g.target_value, "current": g.current_value,
             "progress_pct": g.progress_pct} for g in goals]


@router.post("/goals", status_code=201)
async def create_goal(
    body: dict,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    g = await svc.create_goal(tenant["id"], **body)
    return {"id": g.id, "name": g.name, "metric": g.metric}


@router.delete("/goals/{goal_id}")
async def delete_goal(
    goal_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.delete_goal(goal_id)
    return {"message": "Meta removida."}


# ============================================================
# Alerts
# ============================================================

@router.get("/alerts")
async def list_alerts(
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    svc = _get_service(session)
    alerts = await svc.list_alerts(tenant["id"])
    return [a.__dict__ for a in alerts]


@router.post("/alerts", status_code=201)
async def create_alert(
    body: dict,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    a = await svc.create_alert(tenant["id"], **body)
    return {"id": a.id, "name": a.name, "metric": a.metric}


@router.delete("/alerts/{alert_id}")
async def delete_alert(
    alert_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    svc = _get_service(session)
    await svc.delete_alert(alert_id)
    return {"message": "Alerta removido."}


# ============================================================
# Export
# ============================================================

@router.get("/export/{report_type}")
async def export_report(
    report_type: str,
    tenant: dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session),
    date_from: date = Query(...),
    date_to: date = Query(...),
) -> PlainTextResponse:
    svc = _get_service(session)
    csv_content = await svc.export_csv(tenant["id"], report_type, date_from, date_to)
    return PlainTextResponse(
        csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={report_type}_{date_from}_{date_to}.csv"},
    )
