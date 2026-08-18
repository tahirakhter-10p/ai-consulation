import json
from collections.abc import Sequence

from app.ai.schemas.chat import AIChatMessage
from app.ai.schemas.recommendation import AITreatmentOption

RECOMMENDATION_INSTRUCTIONS = """You provide a non-diagnostic treatment-routing recommendation
for clinical staff. Do not invent facts or state that this is medical advice. Return
only a JSON object with fields \"patient_summary\", \"recommended_treatment_ids\", and optional
\"ai_reasoning\". Select one or two IDs exclusively from the supplied treatment catalog.
Never invent an ID or treatment metadata. The backend resolves all authoritative metadata."""


def build_recommendation_input(
    messages: Sequence[AIChatMessage],
    treatments: Sequence[AITreatmentOption],
) -> str:
    """Format conversation history for recommendation generation."""

    conversation = "\n".join(f"{message.role}: {message.content}" for message in messages)
    catalog = json.dumps([treatment.model_dump(mode="json") for treatment in treatments])
    return f"Treatment catalog:\n{catalog}\n\nConversation:\n{conversation}"
