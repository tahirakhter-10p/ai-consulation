"""Adapters for model providers used exclusively by :class:`AIService`."""

from __future__ import annotations

import json
import re
from typing import Protocol


class AIProvider(Protocol):
    """Minimal provider contract that keeps SDK details out of the AI service."""

    async def generate(self, *, instructions: str, input_text: str) -> str:
        """Generate text from a model using the supplied instructions and input."""


class MockAIProvider:
    """Deterministic provider for local development and tests without credentials."""

    async def generate(self, *, instructions: str, input_text: str) -> str:
        """Return predictable, schema-compatible output for each AI operation."""

        if "JSON object" in instructions and "recommended_treatment_ids" in instructions:
            treatment_ids = re.findall(
                r'"id":\s*"([0-9a-fA-F-]{36})"', input_text.split("Conversation:", 1)[0]
            )
            if not treatment_ids:
                raise RuntimeError("The treatment catalog contains no selectable IDs.")
            return json.dumps(
                {
                    "patient_summary": "The consultation details require clinical review.",
                    "recommended_treatment_ids": treatment_ids[:2],
                    "ai_reasoning": "A clinician should review the reported symptoms and history.",
                }
            )
        return "Thank you for sharing that. Could you provide any additional relevant symptoms?"


class OpenAIProvider:
    """OpenAI Responses API adapter, isolated from business and AI orchestration code."""

    def __init__(self, *, api_key: str, model: str, timeout_seconds: float) -> None:
        self._api_key = api_key
        self._model = model
        self._timeout_seconds = timeout_seconds
        self._client = None

    async def generate(self, *, instructions: str, input_text: str) -> str:
        """Generate text through the asynchronous Responses API."""

        client = self._get_client()
        response = await client.responses.create(
            model=self._model,
            instructions=instructions,
            input=input_text,
        )
        if not response.output_text.strip():
            raise RuntimeError("The AI provider returned an empty response.")
        return response.output_text

    def _get_client(self):
        if self._client is None:
            from openai import AsyncOpenAI

            self._client = AsyncOpenAI(api_key=self._api_key, timeout=self._timeout_seconds)
        return self._client
