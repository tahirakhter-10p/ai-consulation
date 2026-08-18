from decimal import Decimal
from uuid import UUID

from app.schemas.common import ORMResponseModel


class TreatmentResponse(ORMResponseModel):
    """Authoritative treatment metadata exposed to clients."""

    id: UUID
    name: str
    specialty: str
    description: str
    price: Decimal | None
    price_min: Decimal | None
    price_max: Decimal | None
    duration_minutes: int | None
    location: str | None
    default_target_area: str | None
    is_active: bool
