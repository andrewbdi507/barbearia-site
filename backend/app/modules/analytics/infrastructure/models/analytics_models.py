"""Analytics Module — SQLAlchemy Models."""

from __future__ import annotations

from datetime import date as date_type, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, BaseModel


class GoalModel(Base, BaseModel):
    __tablename__ = "analytics_goals"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    metric: Mapped[str] = mapped_column(String(50), nullable=False)
    target_value: Mapped[int] = mapped_column(Integer, default=0)
    current_value: Mapped[int] = mapped_column(Integer, default=0)
    period_start: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    professional_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class AlertRuleModel(Base, BaseModel):
    __tablename__ = "analytics_alerts"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    metric: Mapped[str] = mapped_column(String(50), nullable=False)
    condition: Mapped[str] = mapped_column(Text, default="")
    threshold: Mapped[float] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_triggered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notification_channels: Mapped[list] = mapped_column(JSONB, default=lambda: ["whatsapp"])
