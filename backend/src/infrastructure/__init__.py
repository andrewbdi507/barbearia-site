"""Infrastructure Layer.

The infrastructure layer implements the interfaces defined
in the domain layer. It contains:
- Database (SQLAlchemy engine, session, base model)
- Cache (Redis client)
- HTTP client (httpx)
- External service adapters (payment gateway, email, etc.)

All implementations are concrete adapters that satisfy
domain interface contracts.
"""

from src.infrastructure.database.base import Base
from src.infrastructure.database.session import (
    AsyncSessionFactory,
    get_async_session,
    get_session_factory,
)

__all__ = [
    "AsyncSessionFactory",
    "Base",
    "get_async_session",
    "get_session_factory",
]
