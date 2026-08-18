from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints, model_validator

from app.models.enums import ConsultationStatus
from app.schemas.common import ORMResponseModel

AppointmentText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]


class AppointmentCreateRequest(ORMResponseModel):
    """Payload for booking a consultation appointment."""

    treatment_id: UUID | None = None
    treatment: AppointmentText | None = None
    appointment_datetime: datetime
    location: AppointmentText

    @model_validator(mode="after")
    def require_treatment_reference(self) -> "AppointmentCreateRequest":
        if self.treatment_id is None and self.treatment is None:
            raise ValueError("Either treatment_id or treatment is required.")
        return self


class AppointmentResponse(ORMResponseModel):
    """Appointment entity exposed by the HTTP API."""

    id: UUID
    consultation_id: UUID
    treatment_id: UUID | None
    treatment: str
    specialty: str | None = None
    appointment_datetime: datetime
    location: str
    treatment_description: str | None = None
    default_target_area: str | None = None
    price: Decimal | None = None
    duration_minutes: int | None = None


class AppointmentBookedResponse(ORMResponseModel):
    """Compact response documented for a successful booking."""

    appointment_id: UUID
    consultation_id: UUID
    treatment_id: UUID
    treatment: str
    specialty: str
    treatment_description: str
    default_target_area: str | None = None
    appointment_datetime: datetime
    location: str
    price: Decimal | None = None
    duration_minutes: int | None = None
    status: ConsultationStatus
