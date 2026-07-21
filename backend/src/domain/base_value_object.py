"""Base value object class.

Value objects are immutable, compared by their attributes,
and have no identity. Examples: Money, PhoneNumber, Address.
"""

from __future__ import annotations

from abc import ABC


class BaseValueObject(ABC):
    """Base class for immutable value objects.

    Value objects are defined by their attributes, not identity.
    Two value objects with the same attributes are equal.

    Subclasses should:
    - Be immutable (use @dataclass(frozen=True) or define __init__ carefully)
    - Implement __eq__ and __hash__
    - Validate all attributes in __post_init__ or __init__
    """

    def __repr__(self) -> str:
        attrs = ", ".join(
            f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_")
        )
        return f"{self.__class__.__name__}({attrs})"
