from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints

from app.models.enums import ConsultationStatus
from app.schemas.common import ORMResponseModel

RequiredText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
ShortRequiredText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]


class ConsultationCreateRequest(ORMResponseModel):
    """Payload for creating a consultation."""

    patient_name: ShortRequiredText
    primary_concern: RequiredText


class ConsultationStatusUpdateRequest(ORMResponseModel):
    """Payload for a consultation lifecycle update."""

    status: ConsultationStatus


class ConsultationResponse(ORMResponseModel):
    """Consultation entity exposed by the HTTP API."""

    id: UUID
    patient_name: str
    primary_concern: str
    status: ConsultationStatus


class ConsultationListItemResponse(ConsultationResponse):
    """Consultation list item, including its known recommendation state."""

    recommended_procedure: str = "Pending"
