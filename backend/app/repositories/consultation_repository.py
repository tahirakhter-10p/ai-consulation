from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consultation import Consultation
from app.models.enums import ConsultationStatus


class ConsultationRepository:
    """Persist and retrieve consultation records using an async session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, *, patient_name: str, primary_concern: str) -> Consultation:
        """Add a consultation to the current unit of work and return it."""

        consultation = Consultation(patient_name=patient_name, primary_concern=primary_concern)
        self._session.add(consultation)
        await self._session.flush()
        await self._session.refresh(consultation)
        return consultation

    async def get_by_id(self, consultation_id: UUID) -> Consultation | None:
        """Return one consultation by primary key, if present."""

        return await self._session.get(Consultation, consultation_id)

    async def list(
        self,
        *,
        search: str | None = None,
        status: ConsultationStatus | None = None,
    ) -> list[Consultation]:
        """List consultations, optionally narrowed by patient name and status."""

        statement: Select[tuple[Consultation]] = select(Consultation).order_by(
            Consultation.created_at.desc()
        )
        if search is not None:
            statement = statement.where(
                func.lower(Consultation.patient_name).like(f"%{search.lower()}%")
            )
        if status is not None:
            statement = statement.where(Consultation.status == status)

        result = await self._session.scalars(statement)
        return list(result.all())

    async def search_by_patient_name(self, search: str) -> list[Consultation]:
        """Return consultations whose patient name matches a search term."""

        return await self.list(search=search)

    async def filter_by_status(self, status: ConsultationStatus) -> list[Consultation]:
        """Return consultations in the requested lifecycle state."""

        return await self.list(status=status)

    async def update_status(
        self, consultation_id: UUID, status: ConsultationStatus
    ) -> Consultation | None:
        """Persist a status value for an existing consultation."""

        consultation = await self.get_by_id(consultation_id)
        if consultation is None:
            return None

        consultation.status = status
        await self._session.flush()
        await self._session.refresh(consultation)
        return consultation
