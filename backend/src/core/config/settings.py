"""Application configuration system.

Uses pydantic-settings for type-safe, environment-aware configuration.
Supports: development, testing, staging, production environments.

Architecture:
    Settings is the root configuration object.
    It loads from environment variables and .env files.
    All sub-configs are nested for clean namespacing.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    """Server / Uvicorn configuration."""

    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    workers: int = Field(default=1, alias="WORKERS")


class DatabaseSettings(BaseSettings):
    """PostgreSQL connection configuration."""

    model_config = SettingsConfigDict(env_prefix="DATABASE_", extra="ignore")

    url: str = Field(
        default="postgresql+asyncpg://barbershop:barbershop@localhost:5432/barbershop_dev",
        alias="URL",
    )
    url_sync: str = Field(
        default="postgresql://barbershop:barbershop@localhost:5432/barbershop_dev",
        alias="URL_SYNC",
    )
    pool_size: int = Field(default=20, alias="POOL_SIZE")
    max_overflow: int = Field(default=10, alias="MAX_OVERFLOW")
    pool_timeout: int = Field(default=30, alias="POOL_TIMEOUT")
    echo: bool = Field(default=False, alias="ECHO")


class RedisSettings(BaseSettings):
    """Redis connection configuration."""

    model_config = SettingsConfigDict(env_prefix="REDIS_", extra="ignore")

    url: str = Field(default="redis://localhost:6379/0", alias="URL")
    max_connections: int = Field(default=50, alias="MAX_CONNECTIONS")


class SecuritySettings(BaseSettings):
    """Security configuration — JWT, passwords, CORS."""

    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    secret_key: str = Field(
        default="change-me-to-a-random-secret-key-at-least-32-chars",
        alias="SECRET_KEY",
        min_length=32,
    )
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=15, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_days: int = Field(
        default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS"
    )

    # CORS
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:5173"],
        alias="CORS_ORIGINS",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> list[str]:
        """Parse CORS_ORIGINS from JSON string or list."""
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return [origin.strip() for origin in value.split(",")]
        if isinstance(value, list):
            return [str(origin) for origin in value]
        return ["http://localhost:3000"]


class RateLimitSettings(BaseSettings):
    """Rate limiting configuration."""

    model_config = SettingsConfigDict(env_prefix="RATE_LIMIT_", extra="ignore")

    enabled: bool = Field(default=True, alias="ENABLED")
    default: str = Field(default="100/minute", alias="DEFAULT")
    auth: str = Field(default="5/minute", alias="AUTH")


class LoggingSettings(BaseSettings):
    """Logging configuration."""

    model_config = SettingsConfigDict(env_prefix="LOG_", extra="ignore")

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="DEBUG", alias="LEVEL"
    )
    format: Literal["json", "console"] = Field(default="json", alias="FORMAT")
    colorize: bool = Field(default=False, alias="COLORIZE")


class MonitoringSettings(BaseSettings):
    """Monitoring / observability configuration."""

    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")
    otel_exporter_enabled: bool = Field(default=False, alias="OTEL_EXPORTER_ENABLED")


class Settings(BaseSettings):
    """Root application settings.

    Loads configuration from environment variables and .env file.
    Usage:
        from src.core.config import get_settings
        settings = get_settings()
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    app_env: Literal["development", "testing", "staging", "production"] = Field(
        default="development", alias="APP_ENV"
    )
    app_debug: bool = Field(default=False, alias="APP_DEBUG")
    app_name: str = Field(default="barbershop-saas", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")

    # Sub-configurations
    server: ServerSettings = Field(default_factory=ServerSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    rate_limit: RateLimitSettings = Field(default_factory=RateLimitSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"

    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self.app_env == "testing"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "production"

    @property
    def project_root(self) -> Path:
        """Return the project root directory."""
        return Path(__file__).resolve().parent.parent.parent


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance.

    Uses lru_cache to ensure settings are loaded only once.
    This is the canonical way to access configuration throughout the app.
    """
    return Settings()
