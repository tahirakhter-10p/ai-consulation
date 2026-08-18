from functools import lru_cache

from app.ai.providers.ai_provider import MockAIProvider, OpenAIProvider
from app.ai.service import AIService
from app.core.config import get_settings


@lru_cache
def get_ai_service() -> AIService:
    """Build the configured AI service and its isolated provider adapter."""

    settings = get_settings()
    if settings.ai_provider.lower() == "mock":
        return AIService(MockAIProvider())
    if settings.ai_provider.lower() == "openai":
        if settings.openai_api_key is None:
            raise RuntimeError("OPENAI_API_KEY is required when AI_PROVIDER=openai.")
        return AIService(
            OpenAIProvider(
                api_key=settings.openai_api_key.get_secret_value(),
                model=settings.ai_model,
                timeout_seconds=settings.ai_timeout_seconds,
            )
        )
    raise RuntimeError(f"Unsupported AI provider: {settings.ai_provider}")
