from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.recommendation import Recommendation


class RecommendationRepository:
    """Persist and retrieve a consultation's recommendation record."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(
        self,
        *,
        consultation_id: UUID,
        patient_summary: str,
        recommended_treatments: list[dict[str, object]],
        ai_reasoning: str | None = None,
    ) -> Recommendation:
        """Add a recommendation to the current unit of work and return it."""

        recommendation = Recommendation(
            consultation_id=consultation_id,
            patient_summary=patient_summary,
            recommended_treatments=recommended_treatments,
            ai_reasoning=ai_reasoning,
        )
        self._session.add(recommendation)
        await self._session.flush()
        await self._session.refresh(recommendation)
        return recommendation

    async def get_by_consultation_id(self, consultation_id: UUID) -> Recommendation | None:
        """Return the recommendation for a consultation, if one exists."""

        statement = select(Recommendation).where(Recommendation.consultation_id == consultation_id)
        return await self._session.scalar(statement)
