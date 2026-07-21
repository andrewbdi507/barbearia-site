"""Customer Module — Domain Enums."""

from __future__ import annotations

from enum import StrEnum


class CustomerStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"  # Blacklist
    ANONYMIZED = "anonymized"  # LGPD


class CustomerSource(StrEnum):
    WEBSITE = "website"
    ADMIN = "admin"
    INSTAGRAM = "instagram"
    WHATSAPP = "whatsapp"
    REFERRAL = "referral"
    WALK_IN = "walk_in"
    IMPORT = "import"


class LoyaltyTier(StrEnum):
    BRONZE = "bronze"    # 0-4 visits
    SILVER = "silver"    # 5-14
    GOLD = "gold"        # 15-29
    DIAMOND = "diamond"  # 30+


class LoyaltyTransactionType(StrEnum):
    EARN = "earn"
    REDEEM = "redeem"
    EXPIRE = "expire"
    ADJUSTMENT = "adjustment"
    TIER_UPGRADE = "tier_upgrade"


class ConsentType(StrEnum):
    PRIVACY_POLICY = "privacy_policy"
    TERMS_OF_SERVICE = "terms_of_service"
    MARKETING_EMAILS = "marketing_emails"
    MARKETING_WHATSAPP = "marketing_whatsapp"
    DATA_PROCESSING = "data_processing"


class ReferralStatus(StrEnum):
    PENDING = "pending"
    REGISTERED = "registered"
    BOOKED = "booked"
    REWARDED = "rewarded"
    EXPIRED = "expired"


class ReviewTag(StrEnum):
    PUNCTUAL = "Pontual"
    GREAT_SERVICE = "Atendimento ótimo"
    CLEAN = "Ambiente limpo"
    FRIENDLY = "Atendente simpático"
    FAST = "Rápido"
    RECOMMEND = "Recomendo"
