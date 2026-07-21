"""SQLAlchemy declarative base.

All ORM models MUST inherit from this Base class.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models.

    Provides:
    - Automatic table name generation from class name.
    - Common metadata for all models.
    """

    pass
