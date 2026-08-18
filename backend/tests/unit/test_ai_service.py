from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.ai.providers.ai_provider import MockAIProvider, OpenAIProvider
from app.ai.schemas.chat import AIChatMessage
from app.ai.schemas.recommendation import AITreatmentOption
from app.ai.service import AIService
from app.core.exceptions import AIServiceError, InvalidOperationError

pytestmark = pytest.mark.unit


@pytest.mark.asyncio
async def test_mock_ai_service_generates_valid_chat_and_recommendation() -> None:
    service = AIService(MockAIProvider())
    messages = [AIChatMessage(role="user", content="I have headaches.")]
    treatment = AITreatmentOption(
        id=uuid4(),
        name="Dermal Fillers",
        specialty="Dermatology",
        description="Documented treatment.",
    )

    chat_response = await service.generate_chat_response(messages)
    recommendation = await service.generate_recommendation(messages, [treatment])

    assert chat_response.content
    assert recommendation.patient_summary
    assert recommendation.recommended_treatment_ids == [treatment.id]


@pytest.mark.asyncio
async def test_ai_service_rejects_empty_conversation() -> None:
    service = AIService(MockAIProvider())

    with pytest.raises(InvalidOperationError):
        await service.generate_chat_response([])


@pytest.mark.asyncio
async def test_ai_service_wraps_provider_and_response_validation_errors() -> None:
    messages = [AIChatMessage(role="user", content="Symptoms")]
    failing_provider = SimpleNamespace(generate=AsyncMock(side_effect=RuntimeError("offline")))

    with pytest.raises(AIServiceError):
        await AIService(failing_provider).generate_chat_response(messages)

    blank_provider = SimpleNamespace(generate=AsyncMock(return_value="   "))
    with pytest.raises(AIServiceError):
        await AIService(blank_provider).generate_chat_response(messages)


@pytest.mark.asyncio
async def test_ai_service_validates_recommendation_inputs_and_json() -> None:
    messages = [AIChatMessage(role="user", content="Symptoms")]
    service = AIService(SimpleNamespace(generate=AsyncMock(return_value="not json")))

    with pytest.raises(InvalidOperationError):
        await service.generate_recommendation(messages, [])
    with pytest.raises(AIServiceError):
        await service.generate_recommendation(
            messages,
            [
                AITreatmentOption(
                    id=uuid4(), name="Exam", specialty="General", description="Assessment"
                )
            ],
        )


@pytest.mark.asyncio
async def test_ai_service_accepts_fenced_structured_json() -> None:
    treatment_id = uuid4()
    provider = SimpleNamespace(
        generate=AsyncMock(
            return_value=(
                "```json\n"
                f'{{"patient_summary":"Summary","recommended_treatment_ids":["{treatment_id}"]}}'
                "```"
            )
        )
    )
    service = AIService(provider)
    treatment = AITreatmentOption(
        id=treatment_id, name="Exam", specialty="General", description="Assessment"
    )

    result = await service.generate_recommendation(
        [AIChatMessage(role="user", content="Symptoms")], [treatment]
    )

    assert result.recommended_treatment_ids == [treatment_id]


@pytest.mark.asyncio
async def test_mock_provider_rejects_recommendation_without_treatment_ids() -> None:
    with pytest.raises(RuntimeError):
        await MockAIProvider().generate(
            instructions="Return a JSON object with recommended_treatment_ids",
            input_text="Conversation: symptoms",
        )


@pytest.mark.asyncio
async def test_openai_provider_returns_text_and_rejects_blank_output() -> None:
    provider = OpenAIProvider(api_key="test", model="test-model", timeout_seconds=1)
    create = AsyncMock(return_value=SimpleNamespace(output_text=" response "))
    provider._client = SimpleNamespace(responses=SimpleNamespace(create=create))

    assert await provider.generate(instructions="instructions", input_text="input") == " response "
    create.return_value = SimpleNamespace(output_text=" ")
    with pytest.raises(RuntimeError):
        await provider.generate(instructions="instructions", input_text="input")
