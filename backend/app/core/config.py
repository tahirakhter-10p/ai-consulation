from functools import lru_cache

from pydantic import AnyHttpUrl, Field, PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AI_CONSULTATION_",
        extra="ignore",
    )

    app_name: str = "AI Consultation Platform API"
    app_environment: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    database_url: PostgresDsn
    cors_origins: list[AnyHttpUrl] = Field(default_factory=lambda: ["http://localhost:5173"])
    log_level: str = "INFO"
    ai_provider: str = "mock"
    ai_model: str = "gpt-5-mini"
    ai_timeout_seconds: float = Field(default=30.0, gt=0)
    openai_api_key: SecretStr | None = None

    @computed_field
    @property
    def is_production(self) -> bool:
        return self.app_environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Return the single application settings instance."""

    return Settings()
