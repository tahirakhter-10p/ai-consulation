from collections.abc import Sequence

from app.ai.schemas.chat import AIChatMessage

CONSULTATION_INSTRUCTIONS = """You are a helpful clinical consultation assistant.
Gather relevant information without diagnosing, prescribing treatment, or claiming to
replace a licensed clinician. Encourage urgent medical care for emergency symptoms.
Respond clearly and concisely to the most recent patient message."""


def build_consultation_input(messages: Sequence[AIChatMessage]) -> str:
    """Format persisted conversation history for the chat model."""

    return "\n".join(f"{message.role}: {message.content}" for message in messages)
