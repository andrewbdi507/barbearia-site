"""Base entity class for all domain entities.

All domain entities extend this class. Provides:
- UUID v7 primary key generation
- Equality comparison by identity (not attributes)
- Timestamp tracking
- Dict serialization helper
"""

from __future__ import annotations

import uuid as _uuid
from datetime import datetime, timezone


def generate_entity_id() -> str:
    """Generate a time-ordered UUID v7 for entity identity.

    UUID v7 is preferred over v4 because:
    - Time-ordered → better index locality in databases
    - Non-sequential → safe against enumeration attacks
    """
    try:
        import uuid7

        return str(uuid7.uuid7())
    except ImportError:
        return str(_uuid.uuid4())


class BaseEntity:
    """Base class for all domain entities.

    Entities are distinguished by their identity (id), not attributes.
    Two entities with the same id are considered equal.

    Attributes:
        id: Unique identifier (UUID v7).
        created_at: When this entity was created (UTC).
        updated_at: When this entity was last updated (UTC).
    """

    def __init__(self, entity_id: str | None = None) -> None:
        self.id: str = entity_id or generate_entity_id()
        now = datetime.now(timezone.utc)
        self.created_at: datetime = now
        self.updated_at: datetime = now

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r})"

    def mark_updated(self) -> None:
        """Update the updated_at timestamp to now."""
        self.updated_at = datetime.now(timezone.utc)
