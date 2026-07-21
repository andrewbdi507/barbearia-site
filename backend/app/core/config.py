"""Core Application Settings.

Centraliza TODAS as configurações via Pydantic Settings.
Carrega de .env, variáveis de ambiente e secrets.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class DatabaseSettings(BaseSettings):
    """Configurações de banco de dados."""

    model_config = SettingsConfigDict(env_prefix="DB_")

    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    user: str = Field(default="barbershop")
    password: SecretStr = Field(default=SecretStr("barbershop"))
    name: str = Field(default="barbershop")
    pool_size: int = Field(default=20)
    max_overflow: int = Field(default=10)
    echo: bool = Field(default=False)

    @property
    def dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:"
            f"{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.name}"
        )

    @property
    def sync_dsn(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:"
            f"{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class RedisSettings(BaseSettings):
    """Configurações de Redis (cache + rate limiting)."""

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    password: SecretStr | None = Field(default=None)
    db: int = Field(default=0)
    ssl: bool = Field(default=False)

    @property
    def url(self) -> str:
        proto = "rediss" if self.ssl else "redis"
        auth = ""
        if self.password:
            auth = f":{self.password.get_secret_value()}@"
        return f"{proto}://{auth}{self.host}:{self.port}/{self.db}"


class SecuritySettings(BaseSettings):
    """Configurações de segurança."""

    model_config = SettingsConfigDict(env_prefix="SECURITY_")

    secret_key: SecretStr = Field(
        default=SecretStr("change-me-in-production-32-bytes!!"),
        description="Chave HS256 para JWT — mínimo 32 bytes",
    )
    access_token_expire_minutes: int = Field(
        default=15, ge=5, le=60, description="Expiração do access token JWT"
    )
    refresh_token_expire_days: int = Field(
        default=7, ge=1, le=30, description="Expiração do refresh token"
    )
    max_login_attempts: int = Field(default=5, ge=3, le=10)
    lockout_duration_minutes: int = Field(default=15, ge=5, le=60)
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://localhost:3000"],
    )
    allowed_hosts: list[str] = Field(
        default_factory=lambda: ["*.barbeariaos.com.br", "localhost"],
    )
    bcrypt_rounds: int = Field(default=12, ge=4, le=14)  # legacy, migrando p/ Argon2
    jwt_algorithm: str = Field(default="HS256", description="Algoritmo de assinatura JWT")


class AppSettings(BaseSettings):
    """Configurações da aplicação."""

    model_config = SettingsConfigDict(env_prefix="APP_")

    name: str = Field(default="BarbershopOS")
    env: Literal["development", "staging", "production"] = Field(default="development")
    debug: bool = Field(default=True)
    api_v1_prefix: str = Field(default="/api/v1")
    base_domain: str = Field(default="barbeariaos.com.br")
    default_locale: str = Field(default="pt-BR")
    default_timezone: str = Field(default="America/Sao_Paulo")
    default_currency: str = Field(default="BRL")
    trial_days: int = Field(default=14, ge=7, le=30)
    max_upload_size_mb: int = Field(default=10, ge=1, le=50)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="DEBUG")

    @property
    def is_production(self) -> bool:
        return self.env == "production"

    @property
    def is_development(self) -> bool:
        return self.env == "development"


class Settings(BaseSettings):
    """Agregador de configurações."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)

    # ---- Agents & AI ----
    and_agent_url: str = Field(default="http://and-agent:8000")
    and_agent_enabled: bool = Field(default=True)
    hermes_agent_url: str = Field(default="http://hermes-agent:8000")
    hermes_agent_enabled: bool = Field(default=True)
    evolver_url: str = Field(default="http://evolver-agent:8000")
    evolver_enabled: bool = Field(default=True)
    generic_agent_url: str = Field(default="http://generic-agent:8000")
    generic_agent_enabled: bool = Field(default=True)
    claude_mem_url: str = Field(default="http://claude-mem-agent:8000")
    claude_mem_enabled: bool = Field(default=True)
    agent_timeout: int = Field(default=30)
    agent_retry_attempts: int = Field(default=3)


@lru_cache
def get_settings() -> Settings:
    """Retorna instância singleton das configurações."""
    return Settings()
