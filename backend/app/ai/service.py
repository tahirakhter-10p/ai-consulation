"""Single AI orchestration boundary used by application business services."""

import json
import logging
from collections.abc import Sequence

from pydantic import ValidationError

from app.ai.prompts.consultation import CONSULTATION_INSTRUCTIONS, build_consultation_input
from app.ai.prompts.recommendation import RECOMMENDATION_INSTRUCTIONS, build_recommendation_input
from app.ai.providers.ai_provider import AIProvider
from app.ai.schemas.chat import AIChatMessage, ChatResponse
from app.ai.schemas.recommendation import AIRecommendation, AITreatmentOption
from app.core.exceptions import AIServiceError, InvalidOperationError

logger = logging.getLogger(__name__)


class AIService:
    """Generate chat and structured recommendations through an injected provider."""

    def __init__(self, provider: AIProvider) -> None:
        self._provider = provider

    async def generate_chat_response(self, messages: Sequence[AIChatMessage]) -> ChatResponse:
        """Generate an assistant response for persisted consultation history."""

        self._require_messages(messages)
        content = await self._generate(
            instructions=CONSULTATION_INSTRUCTIONS,
            input_text=build_consultation_input(messages),
        )
        try:
            return ChatResponse(content=content.strip())
        except ValidationError as exc:
            raise AIServiceError from exc

    async def generate_recommendation(
        self,
        messages: Sequence[AIChatMessage],
        treatments: Sequence[AITreatmentOption],
    ) -> AIRecommendation:
        """Generate a structured treatment-routing recommendation."""

        self._require_messages(messages)
        if not treatments:
            raise InvalidOperationError
        content = await self._generate(
            instructions=RECOMMENDATION_INSTRUCTIONS,
            input_text=build_recommendation_input(messages, treatments),
        )
        return self._parse_json(content, AIRecommendation)

    async def _generate(self, *, instructions: str, input_text: str) -> str:
        try:
            return await self._provider.generate(instructions=instructions, input_text=input_text)
        except Exception as exc:
            logger.exception("AI provider generation failed")
            raise AIServiceError from exc

    @staticmethod
    def _parse_json(
        content: str,
        schema: type[AIRecommendation],
    ) -> AIRecommendation:
        normalized_content = content.strip()
        if normalized_content.startswith("```"):
            normalized_content = (
                normalized_content.split("\n", maxsplit=1)[-1].removesuffix("```").strip()
            )
        try:
            return schema.model_validate(json.loads(normalized_content))
        except (json.JSONDecodeError, ValidationError) as exc:
            raise AIServiceError from exc

    @staticmethod
    def _require_messages(messages: Sequence[AIChatMessage]) -> None:
        if not messages:
            raise InvalidOperationError
