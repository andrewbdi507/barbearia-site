"""Database session management for the `app/` module.

Provides:
- get_async_session: FastAPI dependency for request-scoped sessions.
- init_session_factory: Called at application startup.
- close_session_factory: Called at application shutdown.

Architecture:
    The session factory is created once at startup.
    Each request gets its own session via FastAPI dependency injection.
    Sessions are committed on success, rolled back on exception.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


# Global session factory (initialized at startup)
_session_factory: async_sessionmaker[AsyncSession] | None = None
_engine: Any = None


def init_session_factory(settings: Any) -> None:
    """Initialize the async session factory and engine.

    Called once at application startup (lifespan).

    Args:
        settings: Application settings with database configuration.
    """
    global _session_factory, _engine

    db = settings.db
    _engine = create_async_engine(
        db.dsn,
        pool_size=db.pool_size,
        max_overflow=db.max_overflow,
        pool_timeout=getattr(db, "pool_timeout", 30),
        echo=db.echo,
        pool_pre_ping=True,
        connect_args={"ssl": "require"} if "render.com" in db.dsn else {},
    )
    _session_factory = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


async def close_session_factory() -> None:
    """Dispose the engine. Called at application shutdown."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yields a request-scoped database session.

    Usage in route:
        @router.get("/items")
        async def get_items(
            session: AsyncSession = Depends(get_async_session),
        ) -> list[ItemDTO]:
            ...

    The session is automatically committed on success and
    rolled back on exception.
    """
    if _session_factory is None:
        raise RuntimeError(
            "Session factory not initialized. "
            "Call init_session_factory() at startup."
        )

    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
