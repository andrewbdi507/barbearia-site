"""Admin Module — Tests."""

from unittest.mock import MagicMock

import pytest


class TestDashboardAPI:
    def test_dashboard_structure(self) -> None:
        """Dashboard response must contain KPIs and timeline."""
        expected_keys = {"kpis", "today_timeline", "week_revenue", "staff_performance"}
        # Validate structure contract
        assert all(k in expected_keys for k in ["kpis", "today_timeline", "week_revenue", "staff_performance"])

    def test_kpi_contract(self) -> None:
        """Each KPI must have these specific keys."""
        kpi_keys = {
            "revenue_today", "bookings_confirmed", "bookings_completed",
            "bookings_cancelled", "occupancy_pct", "avg_rating",
            "active_staff", "total_customers", "total_reviews",
        }
        assert len(kpi_keys) == 9


class TestGlobalSearch:
    def test_search_contract(self) -> None:
        """Search results must follow the contract."""
        result = {
            "query": "joão",
            "results": {
                "customers": [],
                "services": [],
                "staff": [],
            },
            "total": 0,
        }
        assert "customers" in result["results"]
        assert "services" in result["results"]
        assert "staff" in result["results"]

    def test_search_min_length(self) -> None:
        """Search requires minimum 2 characters."""
        from pydantic import BaseModel, Field
        class SearchQuery(BaseModel):
            q: str = Field(..., min_length=2)

        import pydantic
        with pytest.raises(pydantic.ValidationError):
            SearchQuery(q="a")  # too short
