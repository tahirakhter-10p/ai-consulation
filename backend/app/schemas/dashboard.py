from app.schemas.common import ORMResponseModel


class DashboardStatisticsResponse(ORMResponseModel):
    """Dashboard metrics returned to the administrative client."""

    total_consultations: int
    booked_appointments: int
    conversion_rate: float
