"""Marketing Module — Domain Enums."""

from enum import StrEnum


class CouponType(StrEnum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"


class CouponStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    EXHAUSTED = "exhausted"
    DISABLED = "disabled"


class PromotionType(StrEnum):
    TIME_PERIOD = "time_period"
    HAPPY_HOUR = "happy_hour"
    BUNDLE = "bundle"
    BUY_X_GET_Y = "buy_x_get_y"
    SEASONAL = "seasonal"
    FIRST_PURCHASE = "first_purchase"
    BIRTHDAY = "birthday"


class CampaignStatus(StrEnum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CampaignChannel(StrEnum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    SITE_BANNER = "site_banner"


class SegmentType(StrEnum):
    LAPSED_30D = "lapsed_30d"
    VIP = "vip"
    NEW = "new"
    BIRTHDAY = "birthday"
    HIGH_TICKET = "high_ticket"
    LOW_FREQUENCY = "low_frequency"
    HIGH_CANCELLATION = "high_cancellation"
    CUSTOM = "custom"


class AutomationTrigger(StrEnum):
    CUSTOMER_CREATED = "customer.created"
    BOOKING_COMPLETED = "booking.completed"
    BOOKING_CANCELLED = "booking.cancelled"
    CUSTOMER_LAPSED = "customer.lapsed"
    BIRTHDAY = "customer.birthday"
    PAYMENT_APPROVED = "payment.approved"
    LOYALTY_TIER_CHANGED = "loyalty.tier_changed"
