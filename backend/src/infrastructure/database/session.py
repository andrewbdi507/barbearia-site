"""Database session management.

Provides:
- AsyncSessionFactory: Creates SQLAlchemy async sessions.
- get_async_session: FastAPI dependency for request-scoped sessions.
- Engine creation with connection pooling.

Architecture:
    The session factory is created once at application startup.
    Each request gets its own session via FastAPI dependency injection.
    Sessions are automatically closed when the request ends.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import Settings
from src.core.logging import app_logger

logger = app_logger


class AsyncSessionFactory:
    """Manages SQLAlchemy async engine and session factory.

    Created once at application startup. Provides session-scoped
    database access via get_session().

    Example:
        factory = AsyncSessionFactory(settings)
        async with factory.get_session() as session:
            result = await session.execute(select(...))
    """

    def __init__(self, settings: Settings) -> None:
        self._engine = create_async_engine(
            settings.database.url,
            pool_size=settings.database.pool_size,
            max_overflow=settings.database.max_overflow,
            pool_timeout=settings.database.pool_timeout,
            echo=settings.database.echo,
            pool_pre_ping=True,  # Verify connections before use
        )
        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        logger.info(
            "database_engine_created",
            pool_size=settings.database.pool_size,
            max_overflow=settings.database.max_overflow,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Yield a database session for a single request.

        Usage as FastAPI dependency:
            async def get_db(
                factory: AsyncSessionFactory = Depends(get_session_factory),
            ) -> AsyncGenerator[AsyncSession, None]:
                async with factory.get_session() as session:
                    yield session
        """
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def dispose(self) -> None:
        """Close the engine and release all connections.

        Called during application shutdown.
        """
        await self._engine.dispose()
        logger.info("database_engine_disposed")

    @property
    def engine(self) -> Any:
        """Return the underlying SQLAlchemy engine (for Alembic, etc.)."""
        return self._engine


# Module-level singleton — set during application startup
_session_factory: AsyncSessionFactory | None = None


def init_session_factory(settings: Settings) -> AsyncSessionFactory:
    """Initialize the global session factory.

    MUST be called once during application startup.
    """
    global _session_factory
    _session_factory = AsyncSessionFactory(settings)
    return _session_factory


def get_session_factory() -> AsyncSessionFactory:
    """Return the current session factory.

    Raises RuntimeError if not yet initialized.
    """
    if _session_factory is None:
        raise RuntimeError(
            "Session factory not initialized. "
            "Call init_session_factory() during application startup."
        )
    return _session_factory


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yields a database session per request.

    Usage:
        @router.get("/items")
        async def get_items(
            session: AsyncSession = Depends(get_async_session),
        ):
            ...
    """
    factory = get_session_factory()
    async for session in factory.get_session():
        yield session
