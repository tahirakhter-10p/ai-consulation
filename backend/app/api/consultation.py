from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.responses import STANDARD_ERROR_RESPONSES, success_response
from app.dependencies.services import ConsultationServiceDependency
from app.models.enums import ConsultationStatus
from app.schemas.common import APIResponse
from app.schemas.consultation import (
    ConsultationCreateRequest,
    ConsultationListItemResponse,
    ConsultationResponse,
    ConsultationStatusUpdateRequest,
)
from app.schemas.message import MessageCreateRequest, MessageExchangeResponse, MessageResponse

router = APIRouter(prefix="/consultations", tags=["consultations"])
ConsultationSearchQuery = Annotated[str | None, Query(description="Search by patient name")]
ConsultationStatusQuery = Annotated[ConsultationStatus | None, Query(alias="status")]


@router.post(
    "",
    response_model=APIResponse[ConsultationResponse],
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
    summary="Create consultation",
)
async def create_consultation(
    payload: ConsultationCreateRequest,
    consultation_service: ConsultationServiceDependency,
) -> APIResponse[ConsultationResponse]:
    """Create a consultation through the consultation service."""

    consultation = await consultation_service.create_consultation(
        patient_name=payload.patient_name,
        primary_concern=payload.primary_concern,
    )
    return success_response(
        message="Consultation created successfully.",
        data=ConsultationResponse.model_validate(consultation),
    )


@router.get(
    "",
    response_model=APIResponse[list[ConsultationListItemResponse]],
    responses=STANDARD_ERROR_RESPONSES,
    summary="Get consultations",
)
async def list_consultations(
    consultation_service: ConsultationServiceDependency,
    search: ConsultationSearchQuery = None,
    status_filter: ConsultationStatusQuery = None,
) -> APIResponse[list[ConsultationListItemResponse]]:
    """Return consultations filtered by the documented optional query parameters."""

    consultation_records = await consultation_service.list_consultation_records(
        search=search,
        status=status_filter,
    )
    return success_response(
        message="Consultations retrieved successfully.",
        data=[
            ConsultationListItemResponse(
                id=record.consultation.id,
                patient_name=record.consultation.patient_name,
                primary_concern=record.consultation.primary_concern,
                status=record.consultation.status,
                recommended_procedure=record.recommended_procedure,
            )
            for record in consultation_records
        ],
    )


@router.get(
    "/{consultation_id}",
    response_model=APIResponse[ConsultationResponse],
    responses=STANDARD_ERROR_RESPONSES,
    summary="Get consultation details",
)
async def get_consultation(
    consultation_id: UUID,
    consultation_service: ConsultationServiceDependency,
) -> APIResponse[ConsultationResponse]:
    """Return one consultation through the consultation service."""

    consultation = await consultation_service.get_consultation(consultation_id)
    return success_response(
        message="Consultation retrieved successfully.",
        data=ConsultationResponse.model_validate(consultation),
    )


@router.patch(
    "/{consultation_id}",
    response_model=APIResponse[dict[str, object]],
    responses=STANDARD_ERROR_RESPONSES,
    summary="Update consultation status",
)
async def update_consultation_status(
    consultation_id: UUID,
    payload: ConsultationStatusUpdateRequest,
    consultation_service: ConsultationServiceDependency,
) -> APIResponse[dict[str, object]]:
    """Update one consultation status through the consultation service."""

    await consultation_service.update_status(consultation_id, payload.status)
    return success_response(
        message="Consultation updated successfully.",
        data={},
    )


@router.get(
    "/{consultation_id}/messages",
    response_model=APIResponse[list[MessageResponse]],
    responses=STANDARD_ERROR_RESPONSES,
    summary="Get conversation",
)
async def get_conversation(
    consultation_id: UUID,
    consultation_service: ConsultationServiceDependency,
) -> APIResponse[list[MessageResponse]]:
    """Return persisted conversation history through the consultation service."""

    messages = await consultation_service.get_conversation(consultation_id)
    return success_response(
        message="Conversation retrieved successfully.",
        data=[MessageResponse.model_validate(message) for message in messages],
    )


@router.post(
    "/{consultation_id}/messages",
    response_model=APIResponse[MessageExchangeResponse],
    responses=STANDARD_ERROR_RESPONSES,
    summary="Send consultation message",
)
async def send_message(
    consultation_id: UUID,
    payload: MessageCreateRequest,
    consultation_service: ConsultationServiceDependency,
) -> APIResponse[MessageExchangeResponse]:
    """Persist a user message and its AI response through the consultation service."""

    user_message, assistant_message = await consultation_service.send_message(
        consultation_id=consultation_id,
        message=payload.message,
    )
    return success_response(
        message="Message processed successfully.",
        data=MessageExchangeResponse(
            user_message=MessageResponse.model_validate(user_message),
            assistant_message=MessageResponse.model_validate(assistant_message),
        ),
    )
