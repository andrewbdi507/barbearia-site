"""Customer Module — SQLAlchemy ORM Models.

8 modelos: Customer, CustomerPreference, CustomerTag, Review,
Consent, LoyaltyAccount, LoyaltyTransaction, Referral.
"""

from __future__ import annotations

from datetime import date as date_type
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, BaseModel


class CustomerModel(Base, BaseModel):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    photo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    birth_date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    street: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(2), nullable=True)
    zip_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list] = mapped_column(JSONB, default=list)
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)
    source: Mapped[str] = mapped_column(String(20), default="website")
    total_visits: Mapped[int] = mapped_column(Integer, default=0)
    total_spent: Mapped[int] = mapped_column(Integer, default=0)
    last_visit_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_booking_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("tenant_id", "phone", name="uq_customer_tenant_phone"),
    )

    preferences: Mapped["CustomerPreferenceModel | None"] = relationship(
        "CustomerPreferenceModel", lazy="selectin", back_populates="customer", uselist=False,
    )
    loyalty: Mapped["LoyaltyAccountModel | None"] = relationship(
        "LoyaltyAccountModel", lazy="selectin", back_populates="customer", uselist=False,
    )
    reviews: Mapped[list["ReviewModel"]] = relationship("ReviewModel", back_populates="customer", lazy="selectin")
    consents: Mapped[list["ConsentModel"]] = relationship("ConsentModel", back_populates="customer", lazy="selectin")


class CustomerPreferenceModel(Base, BaseModel):
    __tablename__ = "customer_preferences"

    customer_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, unique=True, index=True,
    )
    favorite_professional_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    favorite_service_ids: Mapped[list] = mapped_column(JSONB, default=list)
    preferred_time: Mapped[str | None] = mapped_column(String(20), nullable=True)
    preferred_day: Mapped[int | None] = mapped_column(Integer, nullable=True)
    communication_preferences: Mapped[dict] = mapped_column(JSONB, default=dict)

    customer: Mapped["CustomerModel"] = relationship("CustomerModel", back_populates="preferences", lazy="selectin")


class CustomerTagModel(Base, BaseModel):
    __tablename__ = "customer_tags"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color_tag: Mapped[str] = mapped_column(String(7), default="#cccccc")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_ctag_tenant_name"),)


class ReviewModel(Base, BaseModel):
    __tablename__ = "customer_reviews"

    booking_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, unique=True, index=True,
    )
    customer_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    professional_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    rating: Mapped[int] = mapped_column(Integer, default=5)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list] = mapped_column(JSONB, default=list)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=False)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)
    business_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    business_response_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    customer: Mapped["CustomerModel"] = relationship("CustomerModel", back_populates="reviews", lazy="selectin")


class ConsentModel(Base, BaseModel):
    __tablename__ = "customer_consents"

    customer_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    consent_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_granted: Mapped[bool] = mapped_column(Boolean, default=True)
    consent_version: Mapped[str] = mapped_column(String(20), default="1.0")
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    customer: Mapped["CustomerModel"] = relationship("CustomerModel", back_populates="consents", lazy="selectin")


class LoyaltyAccountModel(Base, BaseModel):
    __tablename__ = "customer_loyalty"

    customer_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, unique=True, index=True,
    )
    points: Mapped[int] = mapped_column(Integer, default=0)
    total_earned: Mapped[int] = mapped_column(Integer, default=0)
    total_redeemed: Mapped[int] = mapped_column(Integer, default=0)
    tier: Mapped[str] = mapped_column(String(20), default="bronze")
    visit_count: Mapped[int] = mapped_column(Integer, default=0)

    customer: Mapped["CustomerModel"] = relationship("CustomerModel", back_populates="loyalty", lazy="selectin")
    transactions: Mapped[list["LoyaltyTransactionModel"]] = relationship(
        "LoyaltyTransactionModel", lazy="selectin", back_populates="loyalty",
    )


class LoyaltyTransactionModel(Base, BaseModel):
    __tablename__ = "customer_loyalty_transactions"

    loyalty_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("customer_loyalty.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    transaction_type: Mapped[str] = mapped_column(String(20), default="earn")
    points: Mapped[int] = mapped_column(Integer, default=0)
    reference_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reference_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    loyalty: Mapped["LoyaltyAccountModel"] = relationship("LoyaltyAccountModel", back_populates="transactions", lazy="selectin")


class ReferralModel(Base, BaseModel):
    __tablename__ = "customer_referrals"

    referrer_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    referral_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    referred_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    referred_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    referred_customer_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True,
    )
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    reward_granted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
