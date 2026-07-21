"""Marketing Module — Domain Entities.

Coupon, Promotion, Campaign, Automation (Rule Engine), Smart Segment, Gift Card.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class Coupon:
    """Cupom de desconto."""

    id: str
    tenant_id: str
    code: str  # Único por tenant
    coupon_type: str = "fixed"  # fixed, percentage
    value: int = 0  # centavos ou percentual (ex: 2000 = R$20 ou 15 = 15%)
    min_purchase_amount: int = 0  # Valor mínimo da compra
    max_uses: int = 0  # 0 = ilimitado
    current_uses: int = 0
    max_per_customer: int = 1
    starts_at: datetime | None = None
    expires_at: datetime | None = None
    is_active: bool = True
    applies_to: str = "all"  # all, specific_services, specific_professionals
    applicable_ids: list[str] = field(default_factory=list)
    created_by: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_valid(self) -> bool:
        now = datetime.now(timezone.utc)
        if not self.is_active:
            return False
        if self.starts_at and now < self.starts_at:
            return False
        if self.expires_at and now > self.expires_at:
            return False
        if self.max_uses > 0 and self.current_uses >= self.max_uses:
            return False
        return True

    def calculate_discount(self, amount: int) -> int:
        if self.coupon_type == "fixed":
            return min(self.value, amount)
        return int(amount * self.value / 100)

    def apply(self) -> None:
        self.current_uses += 1


@dataclass
class Promotion:
    """Promoção — desconto temporário ou condicional."""

    id: str
    tenant_id: str
    name: str
    promotion_type: str = "time_period"
    description: str = ""
    discount_type: str = "percentage"  # fixed, percentage
    discount_value: int = 0
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    applicable_days: list[int] = field(default_factory=list)  # 0-6, vazio = todos
    applicable_hours_start: str | None = None  # Happy hour
    applicable_hours_end: str | None = None
    service_ids: list[str] = field(default_factory=list)
    bundle_service_ids: list[str] = field(default_factory=list)  # Para tipo "bundle"
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_valid_now(self) -> bool:
        if not self.is_active:
            return False
        now = datetime.now(timezone.utc)
        if self.starts_at and now < self.starts_at:
            return False
        if self.ends_at and now > self.ends_at:
            return False
        if self.applicable_days and now.weekday() not in self.applicable_days:
            return False
        if self.applicable_hours_start and self.applicable_hours_end:
            h = now.hour
            sh = int(self.applicable_hours_start.split(":")[0])
            eh = int(self.applicable_hours_end.split(":")[0])
            if not (sh <= h < eh):
                return False
        return True


@dataclass
class Campaign:
    """Campanha de marketing multi-canal."""

    id: str
    tenant_id: str
    name: str
    description: str = ""
    channel: str = "whatsapp"  # whatsapp, email, sms, push, site_banner
    status: str = "draft"
    segment_type: str = "custom"
    segment_filters: dict[str, Any] = field(default_factory=dict)
    template_id: str | None = None
    coupon_id: str | None = None  # Cupom automático incluso
    scheduled_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    total_sent: int = 0
    total_opened: int = 0
    total_converted: int = 0
    created_by: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AutomationRule:
    """Regra de automação — Event → Condition → Action.

    Rule Engine: eventos disparam workflows.
    """

    id: str
    tenant_id: str
    name: str
    trigger: str  # AutomationTrigger
    is_active: bool = True
    conditions: list[dict[str, Any]] = field(default_factory=list)
    actions: list[dict[str, Any]] = field(default_factory=list)
    # Exemplo de actions:
    # [{"type": "send_coupon", "coupon_id": "c_123", "delay_minutes": 0},
    #  {"type": "wait", "delay_days": 7},
    #  {"type": "send_reminder", "template_id": "t_456", "condition": "not_booked"}]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class GiftCard:
    """Gift Card — vale presente."""

    id: str
    tenant_id: str
    code: str
    initial_amount: int = 0  # centavos
    current_balance: int = 0
    purchaser_customer_id: str | None = None
    recipient_email: str | None = None
    recipient_name: str | None = None
    message: str = ""
    is_redeemed: bool = False
    expires_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def redeem(self, amount: int) -> bool:
        if amount > self.current_balance:
            return False
        self.current_balance -= amount
        if self.current_balance == 0:
            self.is_redeemed = True
        return True
