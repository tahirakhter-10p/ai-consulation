from typing import Literal

from pydantic import BaseModel, Field


class AIChatMessage(BaseModel):
    """A normalized persisted message supplied to the chat model."""

    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)


class ChatResponse(BaseModel):
    """The generated assistant reply returned to the consultation service."""

    content: str = Field(min_length=1)
