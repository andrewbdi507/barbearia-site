"""Analytics Module — Tests."""

import pytest
from datetime import date

from app.modules.analytics.domain.entities import Goal, AlertRule, KPIData, ChartData
from app.modules.analytics.application.kpi_registry import KPI_REGISTRY, register_all_kpis


class TestKPIRegistry:
    def test_all_kpis_registered(self) -> None:
        register_all_kpis()
        assert len(KPI_REGISTRY) >= 6
        assert "revenue_today" in KPI_REGISTRY
        assert "avg_ticket" in KPI_REGISTRY
        assert "occupancy" in KPI_REGISTRY

    def test_kpi_structure(self) -> None:
        register_all_kpis()
        for key, kpi in KPI_REGISTRY.items():
            assert "key" in kpi
            assert "label" in kpi
            assert "format" in kpi
            assert "compute" in kpi
            assert kpi["format"] in ("currency", "percentage", "number", "rating")

    def test_add_new_kpi(self) -> None:
        from app.modules.analytics.application.kpi_registry import register_kpi
        async def dummy_kpi(session, tid, dfrom, dto):
            return KPIData(key="test", label="Test", value=42, format="number")

        register_kpi("test_kpi", "Test KPI", "number", dummy_kpi)
        assert "test_kpi" in KPI_REGISTRY


class TestGoal:
    def test_progress_pct(self) -> None:
        g = Goal(id="g1", tenant_id="t1", name="Meta Receita", metric="revenue",
                 target_value=10000, current_value=7500)
        assert g.progress_pct == 75.0

    def test_progress_100(self) -> None:
        g = Goal(id="g1", tenant_id="t1", name="Meta", metric="bookings",
                 target_value=100, current_value=150)
        assert g.progress_pct == 100.0

    def test_zero_target(self) -> None:
        g = Goal(id="g1", tenant_id="t1", name="Meta", metric="customers",
                 target_value=0, current_value=10)
        assert g.progress_pct == 0


class TestAlertRule:
    def test_create_alert(self) -> None:
        a = AlertRule(id="a1", tenant_id="t1", name="Queda Receita",
                      metric="revenue_drop", condition="revenue < avg * 0.5",
                      threshold=0.5)
        assert a.metric == "revenue_drop"
        assert a.is_active

    def test_notification_channels(self) -> None:
        a = AlertRule(id="a1", tenant_id="t1", name="Test",
                      metric="test", notification_channels=["whatsapp", "email"])
        assert "whatsapp" in a.notification_channels
        assert "email" in a.notification_channels


class TestKPIData:
    def test_kpi_data(self) -> None:
        k = KPIData(key="test", label="Test KPI", value=150.5, format="currency",
                    trend="up", change_pct=12.5)
        assert k.value == 150.5
        assert k.trend == "up"

    def test_kpi_stable(self) -> None:
        k = KPIData(key="test", label="Test", value=50, format="number", trend="stable")
        assert k.trend == "stable"
        assert k.change_pct == 0


class TestChartData:
    def test_chart_data(self) -> None:
        c = ChartData(
            chart_type="bar", title="Top Serviços",
            labels=["Corte", "Barba", "Combo"],
            datasets=[{"label": "Vendas", "data": [50, 30, 20]}],
        )
        assert c.chart_type == "bar"
        assert len(c.labels) == 3
        assert len(c.datasets) == 1


class TestPeriodResolution:
    def test_resolve_period(self) -> None:
        from app.modules.analytics.application.analytics_service import AnalyticsService
        dfrom, dto = AnalyticsService._resolve_period("week")
        assert (dto - dfrom).days == 7

    def test_resolve_custom(self) -> None:
        from app.modules.analytics.application.analytics_service import AnalyticsService
        dfrom, dto = AnalyticsService._resolve_period("custom", date(2026, 1, 1), date(2026, 1, 31))
        assert dfrom == date(2026, 1, 1)
        assert dto == date(2026, 1, 31)
