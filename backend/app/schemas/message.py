from typing import Annotated

from pydantic import StringConstraints

from app.models.enums import MessageRole
from app.schemas.common import ORMResponseModel

MessageText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class MessageCreateRequest(ORMResponseModel):
    """Payload for a user-authored chat message."""

    message: MessageText


class MessageResponse(ORMResponseModel):
    """Persisted conversation message exposed by the HTTP API."""

    role: MessageRole
    content: str


class MessageExchangeResponse(ORMResponseModel):
    """Both persisted sides of one chat interaction."""

    user_message: MessageResponse
    assistant_message: MessageResponse
