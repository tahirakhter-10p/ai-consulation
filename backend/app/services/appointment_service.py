from datetime import datetime
from uuid import UUID

from app.core.exceptions import ConflictError, InvalidOperationError, ResourceNotFoundError
from app.models.appointment import Appointment
from app.models.enums import ConsultationStatus
from app.models.treatment import Treatment
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.consultation_repository import ConsultationRepository
from app.repositories.treatment_repository import TreatmentRepository


class AppointmentService:
    """Coordinate appointment booking with consultation lifecycle updates."""

    def __init__(
        self,
        consultation_repository: ConsultationRepository,
        appointment_repository: AppointmentRepository,
        treatment_repository: TreatmentRepository,
    ) -> None:
        self._consultation_repository = consultation_repository
        self._appointment_repository = appointment_repository
        self._treatment_repository = treatment_repository

    async def book_appointment(
        self,
        *,
        consultation_id: UUID,
        treatment_id: UUID | None,
        treatment: str | None,
        appointment_datetime: datetime,
        location: str,
    ) -> Appointment:
        """Book the single appointment allowed for a consultation and mark it booked."""

        if await self._consultation_repository.get_by_id(consultation_id) is None:
            raise ResourceNotFoundError
        if await self._appointment_repository.get_by_consultation_id(consultation_id):
            raise ConflictError
        if not isinstance(appointment_datetime, datetime):
            raise InvalidOperationError
        treatment_record = await self._resolve_treatment(
            treatment_id=treatment_id,
            treatment_name=treatment,
        )

        appointment = await self._appointment_repository.create(
            consultation_id=consultation_id,
            treatment_id=treatment_record.id,
            treatment=treatment_record.name,
            appointment_datetime=appointment_datetime,
            location=self._required_text(location),
        )
        appointment.treatment_record = treatment_record
        updated_consultation = await self._consultation_repository.update_status(
            consultation_id,
            ConsultationStatus.BOOKED,
        )
        if updated_consultation is None:
            # This should be unreachable after the precondition above, but avoids
            # reporting a successful booking if the consultation was concurrently removed.
            raise ResourceNotFoundError
        return appointment

    async def get_appointments(self) -> list[Appointment]:
        """Return all appointments in scheduled order."""

        return await self._appointment_repository.get_all()

    @staticmethod
    def _required_text(value: str) -> str:
        if not isinstance(value, str) or not (normalized_value := value.strip()):
            raise InvalidOperationError
        return normalized_value

    async def _resolve_treatment(
        self,
        *,
        treatment_id: UUID | None,
        treatment_name: str | None,
    ) -> Treatment:
        treatment = None
        if treatment_id is not None:
            treatment = await self._treatment_repository.get_by_id(treatment_id)
        elif treatment_name is not None:
            treatment = await self._treatment_repository.get_by_name(
                self._required_text(treatment_name)
            )
        if treatment is None:
            raise InvalidOperationError
        return treatment
