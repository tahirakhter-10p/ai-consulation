from uuid import UUID

from fastapi import APIRouter, status

from app.api.responses import STANDARD_ERROR_RESPONSES, success_response
from app.dependencies.services import AppointmentServiceDependency
from app.models.enums import ConsultationStatus
from app.schemas.appointment import (
    AppointmentBookedResponse,
    AppointmentCreateRequest,
    AppointmentResponse,
)
from app.schemas.common import APIResponse

router = APIRouter(tags=["appointments"])


@router.post(
    "/consultations/{consultation_id}/appointment",
    response_model=APIResponse[AppointmentBookedResponse],
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
    summary="Book appointment",
)
async def book_appointment(
    consultation_id: UUID,
    payload: AppointmentCreateRequest,
    appointment_service: AppointmentServiceDependency,
) -> APIResponse[AppointmentBookedResponse]:
    """Book an appointment and update its consultation through the appointment service."""

    appointment = await appointment_service.book_appointment(
        consultation_id=consultation_id,
        treatment_id=payload.treatment_id,
        treatment=payload.treatment,
        appointment_datetime=payload.appointment_datetime,
        location=payload.location,
    )
    return success_response(
        message="Appointment booked successfully.",
        data=AppointmentBookedResponse(
            appointment_id=appointment.id,
            consultation_id=appointment.consultation_id,
            treatment_id=appointment.treatment_id,
            treatment=appointment.treatment,
            specialty=appointment.treatment_record.specialty,
            treatment_description=appointment.treatment_record.description,
            default_target_area=appointment.treatment_record.default_target_area,
            appointment_datetime=appointment.appointment_datetime,
            location=appointment.location,
            price=appointment.treatment_record.price,
            duration_minutes=appointment.treatment_record.duration_minutes,
            status=ConsultationStatus.BOOKED,
        ),
    )


@router.get(
    "/appointments",
    response_model=APIResponse[list[AppointmentResponse]],
    responses=STANDARD_ERROR_RESPONSES,
    summary="Get appointments",
)
async def get_appointments(
    appointment_service: AppointmentServiceDependency,
) -> APIResponse[list[AppointmentResponse]]:
    """Return all appointments through the appointment service."""

    appointments = await appointment_service.get_appointments()
    return success_response(
        message="Appointments retrieved successfully.",
        data=[
            AppointmentResponse(
                id=appointment.id,
                consultation_id=appointment.consultation_id,
                treatment_id=appointment.treatment_id,
                treatment=appointment.treatment,
                specialty=(
                    appointment.treatment_record.specialty
                    if appointment.treatment_record is not None
                    else None
                ),
                appointment_datetime=appointment.appointment_datetime,
                location=appointment.location,
                treatment_description=(
                    appointment.treatment_record.description
                    if appointment.treatment_record is not None
                    else None
                ),
                default_target_area=(
                    appointment.treatment_record.default_target_area
                    if appointment.treatment_record is not None
                    else None
                ),
                price=(
                    appointment.treatment_record.price
                    if appointment.treatment_record is not None
                    else None
                ),
                duration_minutes=(
                    appointment.treatment_record.duration_minutes
                    if appointment.treatment_record is not None
                    else None
                ),
            )
            for appointment in appointments
        ],
    )
