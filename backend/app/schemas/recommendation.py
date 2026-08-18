from decimal import Decimal
from uuid import UUID

from pydantic import Field

from app.schemas.common import ORMResponseModel


class RecommendedTreatment(ORMResponseModel):
    """One structured treatment recommendation."""

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    treatment_id: UUID | None = None
    specialty: str | None = None
    price: Decimal | None = None
    price_min: Decimal | None = None
    price_max: Decimal | None = None
    duration_minutes: int | None = None
    location: str | None = None
    default_target_area: str | None = None
    priority: int | None = None


class RecommendationResponse(ORMResponseModel):
    """Stored structured recommendation for a consultation."""

    patient_summary: str
    recommended_treatments: list[RecommendedTreatment] = Field(min_length=1)
    ai_reasoning: str | None = None
