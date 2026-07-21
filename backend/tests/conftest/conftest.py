"""Test infrastructure — conftest.py

Provides fixtures and utilities for all test modules.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import Settings
from src.infrastructure.database import Base


@pytest.fixture(scope="session")
def event_loop() -> Any:
    """Create a session-scoped event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Return test settings (overrides for test environment)."""
    return Settings(
        app_env="testing",
        app_debug=True,
        database=Settings.model_validate(
            {
                "URL": "postgresql+asyncpg://barbershop:barbershop@localhost:5432/barbershop_test",
                "URL_SYNC": "postgresql://barbershop:barbershop@localhost:5432/barbershop_test",
                "POOL_SIZE": 5,
                "ECHO": False,
            }
        ),
        redis=Settings.model_validate(
            {
                "URL": "redis://localhost:6379/1",
            }
        ),
    )


@pytest.fixture
async def db_session(settings: Settings) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session.

    Creates all tables before the test and drops them after.
    Each test gets a clean database.
    """
    engine = create_async_engine(
        settings.database.url,
        echo=False,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session_factory() as session:
        yield session
        await session.rollback()

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def anyio_backend() -> str:
    """Backend for anyio/pytest-asyncio."""
    return "asyncio"
