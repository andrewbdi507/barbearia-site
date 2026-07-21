"""Analytics Module — Application Service.

KPI Engine, Reports, Goals, Alerts, Comparisons, Exports.
"""

from __future__ import annotations

import csv
import io
from datetime import date, datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.modules.analytics.application.kpi_registry import KPI_REGISTRY, register_all_kpis
from app.modules.analytics.domain.entities import AlertRule, ChartData, Goal, KPIData
from app.modules.analytics.infrastructure.repository import AlertRuleRepository, GoalRepository


class AnalyticsService:
    """Serviço de Analytics & Business Intelligence."""

    def __init__(self, session: AsyncSession) -> None:
        self._s = session
        self._goals = GoalRepository(session)
        self._alerts = AlertRuleRepository(session)
        register_all_kpis()

    # ============================================================
    # KPI Engine
    # ============================================================

    async def compute_kpis(
        self, tenant_id: str, period: str = "today", date_from: date | None = None, date_to: date | None = None,
    ) -> list[KPIData]:
        """Calcula todos os KPIs registrados para o período."""
        dfrom, dto = self._resolve_period(period, date_from, date_to)

        results: list[KPIData] = []
        for key, kpi in KPI_REGISTRY.items():
            try:
                result = await kpi["compute"](self._s, tenant_id, dfrom, dto)
                result.period = period
                results.append(result)
            except Exception:
                results.append(KPIData(
                    key=key, label=kpi["label"], value=0, format=kpi["format"],
                    trend="stable", period=period,
                ))

        return results

    async def get_kpi_list(self) -> list[dict]:
        """Retorna lista de KPIs disponíveis (para o frontend)."""
        return [
            {"key": v["key"], "label": v["label"], "format": v["format"], "description": v["description"]}
            for v in KPI_REGISTRY.values()
        ]

    # ============================================================
    # Charts / Reports
    # ============================================================

    async def revenue_chart(self, tenant_id: str, period: str = "week") -> ChartData:
        """Receita diária no período."""
        dfrom, dto = self._resolve_period(period)
        from app.modules.payment.infrastructure.models.payment_models import PaymentModel

        days = (dto - dfrom).days or 1
        labels: list[str] = []
        values: list[int] = []

        for i in range(days + 1):
            d = dfrom + timedelta(days=i)
            if d > dto:
                break
            labels.append(d.strftime("%d/%m"))
            r = await self._s.execute(
                select(func.coalesce(func.sum(PaymentModel.amount), 0))
                .where(PaymentModel.tenant_id == tenant_id)
                .where(PaymentModel.status == "paid")
                .where(func.date(PaymentModel.paid_at) == d)
            )
            values.append(r.scalar() or 0)

        return ChartData(
            chart_type="line",
            title="Receita",
            labels=labels,
            datasets=[{"label": "Receita (R$)", "data": values, "color": "#1a1a2e"}],
        )

    async def top_services(self, tenant_id: str, limit: int = 5) -> ChartData:
        """Ranking de serviços mais vendidos."""
        from app.modules.scheduling.infrastructure.models.scheduling_models import BookingServiceModel, ServiceModel
        r = await self._s.execute(
            select(ServiceModel.name, func.count(BookingServiceModel.service_id).label("cnt"))
            .join(BookingServiceModel, BookingServiceModel.service_id == ServiceModel.id)
            .where(ServiceModel.tenant_id == tenant_id)
            .group_by(ServiceModel.name)
            .order_by(func.count(BookingServiceModel.service_id).desc())
            .limit(limit)
        )
        rows = r.all()
        return ChartData(
            chart_type="bar",
            title="Top Serviços",
            labels=[row[0] for row in rows],
            datasets=[{"label": "Agendamentos", "data": [row[1] for row in rows], "color": "#e94560"}],
        )

    async def top_professionals(self, tenant_id: str, limit: int = 5) -> ChartData:
        """Ranking de profissionais por receita."""
        from app.modules.scheduling.infrastructure.models.scheduling_models import BookingModel
        from app.modules.staff.infrastructure.models.staff_models import StaffProfileModel
        r = await self._s.execute(
            select(StaffProfileModel.professional_name, func.count(BookingModel.id).label("cnt"))
            .join(BookingModel, BookingModel.professional_id == StaffProfileModel.id)
            .where(BookingModel.tenant_id == tenant_id)
            .where(BookingModel.status.in_(["completed", "confirmed"]))
            .group_by(StaffProfileModel.professional_name)
            .order_by(func.count(BookingModel.id).desc())
            .limit(limit)
        )
        rows = r.all()
        return ChartData(
            chart_type="bar",
            title="Top Profissionais",
            labels=[row[0] for row in rows],
            datasets=[{"label": "Atendimentos", "data": [row[1] for row in rows], "color": "#27ae60"}],
        )

    async def peak_hours(self, tenant_id: str) -> ChartData:
        """Heatmap de horários mais movimentados."""
        from app.modules.scheduling.infrastructure.models.scheduling_models import BookingModel
        r = await self._s.execute(
            select(func.extract("hour", BookingModel.start_time).label("h"), func.count().label("cnt"))
            .where(BookingModel.tenant_id == tenant_id)
            .where(BookingModel.status.in_(["completed", "confirmed"]))
            .group_by("h").order_by("h")
        )
        rows = r.all()
        hours = list(range(8, 21))
        data = [0] * len(hours)
        for row in rows:
            h = int(float(row[0]))
            if h in hours:
                data[hours.index(h)] = row[1]
        return ChartData(
            chart_type="bar",
            title="Horários de Pico",
            labels=[f"{h}h" for h in hours],
            datasets=[{"label": "Atendimentos", "data": data, "color": "#f39c12"}],
        )

    # ============================================================
    # Goals
    # ============================================================

    async def list_goals(self, tenant_id: str) -> list[Goal]:
        return await self._goals.list_by_tenant(tenant_id)

    async def create_goal(self, tenant_id: str, **kwargs: object) -> Goal:
        goal = Goal(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            metric=str(kwargs["metric"]),
            target_value=int(kwargs.get("target_value", 0)),
            period_start=kwargs.get("period_start"),
            period_end=kwargs.get("period_end"),
            professional_id=str(kwargs.get("professional_id", "")) if kwargs.get("professional_id") else None,
        )
        return await self._goals.create(goal)

    async def delete_goal(self, goal_id: str) -> None:
        await self._goals.delete(goal_id)

    # ============================================================
    # Alerts
    # ============================================================

    async def list_alerts(self, tenant_id: str) -> list[AlertRule]:
        return await self._alerts.list_active(tenant_id)

    async def create_alert(self, tenant_id: str, **kwargs: object) -> AlertRule:
        alert = AlertRule(
            id=str(uuid4()), tenant_id=tenant_id,
            name=str(kwargs["name"]),
            metric=str(kwargs["metric"]),
            condition=str(kwargs.get("condition", "")),
            threshold=float(kwargs.get("threshold", 0)),
            notification_channels=list(kwargs.get("notification_channels", ["whatsapp"])),
        )
        return await self._alerts.create(alert)

    async def evaluate_alerts(self, tenant_id: str) -> list[dict]:
        """Avalia todas as regras de alerta ativas."""
        alerts = await self._alerts.list_active(tenant_id)
        triggered: list[dict] = []

        # Simplified evaluation — in production, evaluate against real metrics
        for alert in alerts:
            # Check if alert should trigger (simplified)
            triggered.append({
                "alert_id": alert.id,
                "name": alert.name,
                "metric": alert.metric,
                "triggered": False,
            })

        return triggered

    async def delete_alert(self, alert_id: str) -> None:
        await self._alerts.delete(alert_id)

    # ============================================================
    # Export
    # ============================================================

    async def export_csv(self, tenant_id: str, report_type: str, date_from: date, date_to: date) -> str:
        """Exporta relatório em CSV."""
        output = io.StringIO()
        writer = csv.writer(output)

        if report_type == "bookings":
            from app.modules.scheduling.infrastructure.models.scheduling_models import BookingModel
            r = await self._s.execute(
                select(BookingModel).where(
                    BookingModel.tenant_id == tenant_id,
                    BookingModel.booking_date >= date_from,
                    BookingModel.booking_date <= date_to,
                ).order_by(BookingModel.booking_date, BookingModel.start_time)
            )
            writer.writerow(["Data", "Hora", "Cliente", "Profissional", "Status", "Valor"])
            for b in r.scalars().all():
                writer.writerow([b.booking_date, b.start_time, b.guest_name or "", "", b.status, b.total_amount])

        elif report_type == "revenue":
            from app.modules.payment.infrastructure.models.payment_models import PaymentModel
            r = await self._s.execute(
                select(PaymentModel).where(
                    PaymentModel.tenant_id == tenant_id, PaymentModel.status == "paid",
                ).where(func.date(PaymentModel.paid_at) >= date_from).where(func.date(PaymentModel.paid_at) <= date_to)
            )
            writer.writerow(["Data", "Valor (R$)", "Método", "Gateway"])
            for p in r.scalars().all():
                writer.writerow([p.paid_at, f"{(p.amount / 100):.2f}", p.payment_method, p.gateway])

        elif report_type == "customers":
            from app.modules.customer.infrastructure.models.customer_models import CustomerModel
            r = await self._s.execute(
                select(CustomerModel).where(CustomerModel.tenant_id == tenant_id, CustomerModel.deleted_at.is_(None))
            )
            writer.writerow(["Nome", "Telefone", "Email", "Visitas", "Total Gasto", "Cadastro"])
            for c in r.scalars().all():
                writer.writerow([c.name, c.phone, c.email, c.total_visits, f"{(c.total_spent / 100):.2f}", c.created_at])

        return output.getvalue()

    # ============================================================
    # Helpers
    # ============================================================

    @staticmethod
    def _resolve_period(period: str, dfrom: date | None = None, dto: date | None = None) -> tuple[date, date]:
        today = date.today()
        if dfrom and dto:
            return dfrom, dto

        mapping = {
            "today": (today, today),
            "yesterday": (today - timedelta(days=1), today - timedelta(days=1)),
            "week": (today - timedelta(days=7), today),
            "month": (today - timedelta(days=30), today),
            "year": (today - timedelta(days=365), today),
        }
        return mapping.get(period, (today, today))
