"""Scheduling Module — SQLAlchemy ORM Models.

9 modelos: ServiceCategory, Service, ProfessionalService,
Booking, BookingService, BookingStatusLog, BlockedDate, WaitlistEntry.
"""

from __future__ import annotations

from datetime import date as date_type
from datetime import datetime, time, timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Integer, String, Text, Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, BaseModel


class ServiceCategoryModel(Base, BaseModel):
    __tablename__ = "service_categories"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    color_tag: Mapped[str] = mapped_column(String(7), default="#cccccc")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_svc_cat_tenant_name"),)

    services: Mapped[list["ServiceModel"]] = relationship("ServiceModel", back_populates="category", lazy="selectin")


class ServiceModel(Base, BaseModel):
    __tablename__ = "services"

    category_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("service_categories.id", ondelete="SET NULL"), nullable=True, index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    buffer_minutes: Mapped[int] = mapped_column(Integer, default=0)
    base_price: Mapped[int] = mapped_column(Integer, default=0)  # centavos
    promotional_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    requires_deposit: Mapped[bool] = mapped_column(Boolean, default=False)
    deposit_value: Mapped[int] = mapped_column(Integer, default=0)
    color_tag: Mapped[str] = mapped_column(String(7), default="#cccccc")
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    min_advance_minutes: Mapped[int] = mapped_column(Integer, default=0)
    max_advance_days: Mapped[int] = mapped_column(Integer, default=90)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    category: Mapped[ServiceCategoryModel | None] = relationship("ServiceCategoryModel", back_populates="services", lazy="selectin")
    professional_links: Mapped[list["ProfessionalServiceModel"]] = relationship("ProfessionalServiceModel", back_populates="service", lazy="selectin")


class ProfessionalServiceModel(Base, BaseModel):
    __tablename__ = "professional_services"

    professional_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("staff_profiles.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    service_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    custom_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    custom_duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (UniqueConstraint("professional_id", "service_id", name="uq_prof_svc"),)

    service: Mapped["ServiceModel"] = relationship("ServiceModel", back_populates="professional_links", lazy="selectin")


class BookingModel(Base, BaseModel):
    __tablename__ = "bookings"

    professional_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("staff_profiles.id", ondelete="RESTRICT"), nullable=False, index=True,
    )
    customer_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    booking_date: Mapped[date_type] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    guest_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    guest_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    guest_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_amount: Mapped[int] = mapped_column(Integer, default=0)
    total_duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    discount_amount: Mapped[int] = mapped_column(Integer, default=0)
    source: Mapped[str] = mapped_column(String(20), default="website")
    idempotency_key: Mapped[str | None] = mapped_column(
        String(100), nullable=True, unique=True, index=True,
    )
    created_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    checked_in_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rescheduled_from_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    rescheduled_to_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)

    __table_args__ = (
        UniqueConstraint(
            "professional_id", "booking_date", "start_time",
            name="uq_booking_no_double",
        ),
    )

    booking_services: Mapped[list["BookingServiceModel"]] = relationship("BookingServiceModel", back_populates="booking", lazy="selectin")
    status_logs: Mapped[list["BookingStatusLogModel"]] = relationship("BookingStatusLogModel", back_populates="booking", lazy="selectin")


class BookingServiceModel(Base, BaseModel):
    __tablename__ = "booking_services"

    booking_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("bookings.id", ondelete="CASCADE"), primary_key=True,
    )
    service_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("services.id", ondelete="RESTRICT"), primary_key=True,
    )
    service_name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[int] = mapped_column(Integer, default=0)  # snapshot em centavos
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)  # snapshot

    booking: Mapped["BookingModel"] = relationship("BookingModel", back_populates="booking_services", lazy="selectin")


class BookingStatusLogModel(Base, BaseModel):
    __tablename__ = "booking_status_logs"

    booking_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    from_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    to_status: Mapped[str] = mapped_column(String(20), nullable=False)
    changed_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    booking: Mapped["BookingModel"] = relationship("BookingModel", back_populates="status_logs", lazy="selectin")


class BlockedDateModel(Base, BaseModel):
    __tablename__ = "blocked_dates"

    blocked_date: Mapped[date_type] = mapped_column(Date, nullable=False, index=True)
    professional_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("staff_profiles.id", ondelete="CASCADE"), nullable=True, index=True,
    )
    block_type: Mapped[str] = mapped_column(String(20), default="full_day")
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    start_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    end_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    recurring_pattern: Mapped[str | None] = mapped_column(String(20), nullable=True)
    recurring_until: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(36), nullable=True)


class WaitlistEntryModel(Base, BaseModel):
    __tablename__ = "waitlist_entries"

    customer_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    guest_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    guest_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    professional_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("staff_profiles.id", ondelete="SET NULL"), nullable=True, index=True,
    )
    service_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("services.id", ondelete="SET NULL"), nullable=True,
    )
    desired_date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    desired_period: Mapped[str] = mapped_column(String(20), default="any")
    status: Mapped[str] = mapped_column(String(20), default="waiting", index=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
    notified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
