from fastapi import APIRouter

from app.api.responses import STANDARD_ERROR_RESPONSES, success_response
from app.dependencies.services import DashboardServiceDependency
from app.schemas.common import APIResponse
from app.schemas.dashboard import DashboardStatisticsResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get(
    "",
    response_model=APIResponse[DashboardStatisticsResponse],
    responses=STANDARD_ERROR_RESPONSES,
    summary="Get dashboard statistics",
)
async def get_dashboard_statistics(
    dashboard_service: DashboardServiceDependency,
) -> APIResponse[DashboardStatisticsResponse]:
    """Return the dashboard metrics calculated by the dashboard service."""

    statistics = await dashboard_service.get_statistics()
    return success_response(
        message="Dashboard statistics retrieved successfully.",
        data=DashboardStatisticsResponse.model_validate(statistics),
    )
