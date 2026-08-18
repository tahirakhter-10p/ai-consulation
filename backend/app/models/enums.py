from enum import StrEnum


class ConsultationStatus(StrEnum):
    """Allowed lifecycle states for a consultation."""

    PENDING = "Pending"
    BOOKED = "Booked"
    COMPLETED = "Completed"


class MessageRole(StrEnum):
    """Actors that can author a consultation message."""

    USER = "user"
    ASSISTANT = "assistant"
