from uuid import UUID

from fastapi import APIRouter, status

from app.api.responses import STANDARD_ERROR_RESPONSES, success_response
from app.dependencies.services import RecommendationServiceDependency
from app.schemas.common import APIResponse
from app.schemas.recommendation import RecommendationResponse

router = APIRouter(prefix="/consultations", tags=["recommendations"])


@router.post(
    "/{consultation_id}/recommendation",
    response_model=APIResponse[RecommendationResponse],
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
    summary="Generate recommendation",
)
async def generate_recommendation(
    consultation_id: UUID,
    recommendation_service: RecommendationServiceDependency,
) -> APIResponse[RecommendationResponse]:
    """Generate and store a structured recommendation."""

    recommendation = await recommendation_service.generate_recommendation(
        consultation_id=consultation_id
    )
    return success_response(
        message="Recommendation generated successfully.",
        data=RecommendationResponse.model_validate(recommendation),
    )


@router.get(
    "/{consultation_id}/recommendation",
    response_model=APIResponse[RecommendationResponse],
    responses=STANDARD_ERROR_RESPONSES,
    summary="Get recommendation",
)
async def get_recommendation(
    consultation_id: UUID,
    recommendation_service: RecommendationServiceDependency,
) -> APIResponse[RecommendationResponse]:
    """Return a stored structured recommendation."""

    recommendation = await recommendation_service.get_recommendation(consultation_id)
    return success_response(
        message="Recommendation retrieved successfully.",
        data=RecommendationResponse.model_validate(recommendation),
    )
