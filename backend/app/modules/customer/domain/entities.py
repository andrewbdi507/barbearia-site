"""Customer Module — Domain Entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Any
from uuid import uuid4

from app.modules.customer.domain.enums import (
    ConsentType,
    CustomerSource,
    CustomerStatus,
    LoyaltyTier,
    LoyaltyTransactionType,
    ReferralStatus,
)


@dataclass
class Customer:
    """Aggregate Root — Cliente final da barbearia."""

    id: str
    tenant_id: str
    name: str
    phone: str | None = None
    email: str | None = None
    photo_url: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    notes: str | None = None
    tags: list[str] = field(default_factory=list)
    status: CustomerStatus = CustomerStatus.ACTIVE
    source: CustomerSource = CustomerSource.WEBSITE
    total_visits: int = 0
    total_spent: int = 0
    last_visit_at: datetime | None = None
    last_booking_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = None

    @property
    def is_active(self) -> bool:
        return self.status == CustomerStatus.ACTIVE

    @property
    def is_blocked(self) -> bool:
        return self.status == CustomerStatus.BLOCKED

    def block(self, reason: str) -> None:
        self.status = CustomerStatus.BLOCKED
        self.notes = f"{self.notes or ''}\n[BLOQUEADO] {reason}"

    def unblock(self) -> None:
        self.status = CustomerStatus.ACTIVE

    def anonymize(self) -> None:
        self.status = CustomerStatus.ANONYMIZED
        self.name = "ANONYMIZED"
        self.email = None
        self.phone = None
        self.photo_url = None

    def record_visit(self, amount: int = 0) -> None:
        self.total_visits += 1
        self.total_spent += amount
        self.last_visit_at = datetime.now(timezone.utc)


@dataclass
class CustomerPreference:
    """Preferências do cliente (1:1)."""

    id: str
    customer_id: str
    favorite_professional_id: str | None = None
    favorite_service_ids: list[str] = field(default_factory=list)
    preferred_time: str | None = None  # "morning", "afternoon", "evening"
    preferred_day: int | None = None  # 0=Monday
    communication_preferences: dict[str, bool] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class CustomerTag:
    """Tag configurável por tenant."""

    id: str
    tenant_id: str
    name: str
    color_tag: str = "#cccccc"
    description: str = ""
    is_system: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Review:
    """Avaliação pós-atendimento."""

    id: str
    tenant_id: str
    booking_id: str
    customer_id: str
    professional_id: str
    rating: int = 5  # 1-5
    comment: str | None = None
    tags: list[str] = field(default_factory=list)
    is_visible: bool = False  # Moderado
    is_anonymous: bool = False
    business_response: str | None = None
    business_response_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def moderate(self, approved: bool) -> None:
        self.is_visible = approved

    def respond(self, response: str) -> None:
        self.business_response = response
        self.business_response_at = datetime.now(timezone.utc)


@dataclass
class Consent:
    """Registro de consentimento LGPD (append-only)."""

    id: str
    tenant_id: str
    customer_id: str
    consent_type: ConsentType = ConsentType.PRIVACY_POLICY
    is_granted: bool = True
    consent_version: str = "1.0"
    ip_address: str | None = None
    user_agent: str | None = None
    granted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    revoked_at: datetime | None = None

    def revoke(self) -> None:
        self.is_granted = False
        self.revoked_at = datetime.now(timezone.utc)


@dataclass
class LoyaltyAccount:
    """Conta de fidelidade do cliente (1:1)."""

    id: str
    tenant_id: str
    customer_id: str
    points: int = 0
    total_earned: int = 0
    total_redeemed: int = 0
    tier: LoyaltyTier = LoyaltyTier.BRONZE
    visit_count: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def earn(self, points: int, visit: bool = False) -> "LoyaltyTransaction":
        self.points += points
        self.total_earned += points
        if visit:
            self.visit_count += 1
        self._recalculate_tier()
        return LoyaltyTransaction(
            id=str(uuid4()), loyalty_id=self.id,
            transaction_type=LoyaltyTransactionType.EARN,
            points=points, description="Pontos ganhos",
        )

    def redeem(self, points: int, description: str = "") -> "LoyaltyTransaction":
        if points > self.points:
            raise ValueError("Pontos insuficientes.")
        self.points -= points
        self.total_redeemed += points
        return LoyaltyTransaction(
            id=str(uuid4()), loyalty_id=self.id,
            transaction_type=LoyaltyTransactionType.REDEEM,
            points=-points, description=description,
        )

    def _recalculate_tier(self) -> None:
        old = self.tier
        if self.visit_count >= 30:
            self.tier = LoyaltyTier.DIAMOND
        elif self.visit_count >= 15:
            self.tier = LoyaltyTier.GOLD
        elif self.visit_count >= 5:
            self.tier = LoyaltyTier.SILVER
        else:
            self.tier = LoyaltyTier.BRONZE

        if self.tier != old:
            self.updated_at = datetime.now(timezone.utc)


@dataclass
class LoyaltyTransaction:
    """Histórico de transações de fidelidade (append-only)."""

    id: str
    loyalty_id: str
    transaction_type: LoyaltyTransactionType = LoyaltyTransactionType.EARN
    points: int = 0
    reference_type: str | None = None
    reference_id: str | None = None
    description: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Referral:
    """Programa de indicação."""

    id: str
    tenant_id: str
    referrer_id: str  # Customer que indicou
    referral_code: str
    referred_name: str | None = None
    referred_phone: str | None = None
    referred_customer_id: str | None = None  # Customer do indicado (quando criar conta)
    status: ReferralStatus = ReferralStatus.PENDING
    reward_granted_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def mark_registered(self, referred_customer_id: str) -> None:
        self.referred_customer_id = referred_customer_id
        self.status = ReferralStatus.REGISTERED

    def mark_booked(self) -> None:
        self.status = ReferralStatus.BOOKED

    def mark_rewarded(self) -> None:
        self.status = ReferralStatus.REWARDED
        self.reward_granted_at = datetime.now(timezone.utc)
