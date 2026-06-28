"""Centralized application configuration.

All configuration is sourced from environment variables (.env in local
development). No secret values are hardcoded here, per Engineering Rules §6.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from the environment."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = Field(default="development", alias="APP_ENV")
    app_name: str = Field(default="real-estate-ai-backend", alias="APP_NAME")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    database_url: str = Field(
        default="postgresql+asyncpg://real_estate_ai:change-me@localhost:5432/real_estate_ai",
        alias="DATABASE_URL",
    )

    whatsapp_provider: str = Field(default="whatsapp_web", alias="WHATSAPP_PROVIDER")
    whatsapp_session_path: str = Field(
        default="/data/whatsapp-session", alias="WHATSAPP_SESSION_PATH"
    )
    whatsapp_session_encryption_key: str = Field(
        default="", alias="WHATSAPP_SESSION_ENCRYPTION_KEY"
    )

    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
