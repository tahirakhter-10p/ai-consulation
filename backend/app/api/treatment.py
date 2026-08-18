from fastapi import APIRouter

from app.api.responses import STANDARD_ERROR_RESPONSES, success_response
from app.dependencies.services import TreatmentServiceDependency
from app.schemas.common import APIResponse
from app.schemas.treatment import TreatmentResponse

router = APIRouter(prefix="/treatments", tags=["treatments"])


@router.get(
    "",
    response_model=APIResponse[list[TreatmentResponse]],
    responses=STANDARD_ERROR_RESPONSES,
    summary="Get treatment catalog",
)
async def get_treatments(
    treatment_service: TreatmentServiceDependency,
) -> APIResponse[list[TreatmentResponse]]:
    treatments = await treatment_service.list_treatments()
    return success_response(
        message="Treatments retrieved successfully.",
        data=[TreatmentResponse.model_validate(treatment) for treatment in treatments],
    )
