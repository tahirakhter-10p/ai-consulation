from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.treatment import Treatment


class TreatmentRepository:
    """Read authoritative treatment metadata for recommendation and booking workflows."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_active(self) -> list[Treatment]:
        """Return only active treatments in display order."""

        statement = (
            select(Treatment).where(Treatment.is_active.is_(True)).order_by(Treatment.name.asc())
        )
        result = await self._session.scalars(statement)
        return list(result.all())

    async def get_by_id(self, treatment_id: UUID) -> Treatment | None:
        statement = select(Treatment).where(
            Treatment.id == treatment_id, Treatment.is_active.is_(True)
        )
        return await self._session.scalar(statement)

    async def get_by_ids(self, treatment_ids: list[UUID]) -> list[Treatment]:
        if not treatment_ids:
            return []
        statement = select(Treatment).where(
            Treatment.id.in_(treatment_ids), Treatment.is_active.is_(True)
        )
        result = await self._session.scalars(statement)
        return list(result.all())

    async def get_by_name(self, name: str) -> Treatment | None:
        statement = select(Treatment).where(
            func.lower(Treatment.name) == name.strip().lower(), Treatment.is_active.is_(True)
        )
        return await self._session.scalar(statement)
