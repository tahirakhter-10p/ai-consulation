from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.appointment import Appointment


class AppointmentRepository:
    """Persist and retrieve appointment records using an async session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        consultation_id: UUID,
        treatment_id: UUID,
        treatment: str,
        appointment_datetime: datetime,
        location: str,
    ) -> Appointment:
        """Add an appointment to the current unit of work and return it."""

        appointment = Appointment(
            consultation_id=consultation_id,
            treatment_id=treatment_id,
            treatment=treatment,
            appointment_datetime=appointment_datetime,
            location=location,
        )
        self._session.add(appointment)
        await self._session.flush()
        await self._session.refresh(appointment)
        return appointment

    async def get_all(self) -> list[Appointment]:
        """Return appointments in ascending scheduled order."""

        statement = (
            select(Appointment)
            .options(selectinload(Appointment.treatment_record))
            .order_by(Appointment.appointment_datetime.asc())
        )
        result = await self._session.scalars(statement)
        return list(result.all())

    async def get_by_consultation_id(self, consultation_id: UUID) -> Appointment | None:
        """Return the appointment associated with a consultation, if present."""

        statement = (
            select(Appointment)
            .options(selectinload(Appointment.treatment_record))
            .where(Appointment.consultation_id == consultation_id)
        )
        return await self._session.scalar(statement)
