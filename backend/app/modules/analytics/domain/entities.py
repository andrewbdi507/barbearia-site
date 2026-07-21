"""Analytics Module — Domain Entities.

Goal, Alert, Report, KPIDefinition.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class Goal:
    """Meta de negócio — receita, clientes, atendimentos."""

    id: str
    tenant_id: str
    name: str
    metric: str  # "revenue", "customers", "bookings", "avg_ticket"
    target_value: int = 0  # centavos para revenue, inteiro para resto
    current_value: int = 0
    period_start: date | None = None
    period_end: date | None = None
    professional_id: str | None = None  # Meta por profissional (opcional)
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def progress_pct(self) -> float:
        if self.target_value == 0:
            return 0
        return min(100, round(self.current_value / self.target_value * 100, 1))


@dataclass
class AlertRule:
    """Regra de alerta inteligente."""

    id: str
    tenant_id: str
    name: str
    metric: str  # "revenue_drop", "cancellation_spike", "staff_idle", "churn_risk"
    condition: str  # "revenue_daily < avg_weekly * 0.5"
    threshold: float = 0
    is_active: bool = True
    last_triggered_at: datetime | None = None
    notification_channels: list[str] = field(default_factory=lambda: ["whatsapp"])
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class KPIData:
    """Resultado de um KPI calculado."""

    name: str
    label: str
    value: float
    format: str = "number"  # "currency", "percentage", "number", "rating"
    trend: str = "stable"  # "up", "down", "stable"
    change_pct: float = 0
    vs_last_period: float = 0
    period: str = "today"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChartData:
    """Dados formatados para gráfico."""

    chart_type: str  # "line", "bar", "pie", "area", "heatmap", "table"
    title: str
    labels: list[str] = field(default_factory=list)
    datasets: list[dict[str, Any]] = field(default_factory=list)
    options: dict[str, Any] = field(default_factory=dict)
