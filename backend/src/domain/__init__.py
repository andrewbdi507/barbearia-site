"""Domain Layer.

The domain layer contains the enterprise business rules.
Entities, value objects, aggregates, and repository interfaces
live here.

This layer has ZERO dependencies on frameworks, databases,
or any external concern. It is pure Python.

Currently empty — domain entities will be added in future prompts.
"""

from src.domain.base_entity import BaseEntity
from src.domain.base_value_object import BaseValueObject

__all__ = ["BaseEntity", "BaseValueObject"]
