from uuid import UUID

from app.ai.schemas.chat import AIChatMessage
from app.ai.schemas.recommendation import AITreatmentOption
from app.ai.service import AIService
from app.core.exceptions import (
    AIServiceError,
    ConflictError,
    InvalidOperationError,
    ResourceNotFoundError,
)
from app.models.recommendation import Recommendation
from app.models.treatment import Treatment
from app.repositories.consultation_repository import ConsultationRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.treatment_repository import TreatmentRepository


class RecommendationService:
    """Manage the one generated recommendation associated with a consultation."""

    def __init__(
        self,
        consultation_repository: ConsultationRepository,
        message_repository: MessageRepository,
        recommendation_repository: RecommendationRepository,
        treatment_repository: TreatmentRepository,
        ai_service: AIService,
    ) -> None:
        self._consultation_repository = consultation_repository
        self._message_repository = message_repository
        self._recommendation_repository = recommendation_repository
        self._treatment_repository = treatment_repository
        self._ai_service = ai_service

    async def generate_recommendation(
        self,
        *,
        consultation_id: UUID,
    ) -> Recommendation:
        """Generate and persist the single recommendation for a consultation."""

        await self._get_existing_consultation(consultation_id)
        existing_recommendation = await self._recommendation_repository.get_by_consultation_id(
            consultation_id
        )
        if existing_recommendation is not None:
            raise ConflictError
        conversation = await self._message_repository.get_conversation(consultation_id)
        ai_messages = [
            AIChatMessage(role=message.role.value, content=message.content)
            for message in conversation
        ]
        treatments = await self._treatment_repository.list_active()
        if not treatments:
            raise InvalidOperationError
        ai_recommendation = await self._ai_service.generate_recommendation(
            ai_messages,
            [
                AITreatmentOption(
                    id=treatment.id,
                    name=treatment.name,
                    specialty=treatment.specialty,
                    description=treatment.description,
                )
                for treatment in treatments
            ],
        )
        selected_ids = ai_recommendation.recommended_treatment_ids
        if len(selected_ids) != len(set(selected_ids)):
            raise AIServiceError
        selected_treatments = await self._treatment_repository.get_by_ids(selected_ids)
        treatments_by_id = {treatment.id: treatment for treatment in selected_treatments}
        if any(treatment_id not in treatments_by_id for treatment_id in selected_ids):
            raise AIServiceError

        return await self._recommendation_repository.save(
            consultation_id=consultation_id,
            patient_summary=ai_recommendation.patient_summary,
            recommended_treatments=[
                self._treatment_snapshot(treatments_by_id[treatment_id], priority=index)
                for index, treatment_id in enumerate(selected_ids, start=1)
            ],
            ai_reasoning=ai_recommendation.ai_reasoning,
        )

    async def get_recommendation(self, consultation_id: UUID) -> Recommendation:
        """Return a consultation's recommendation or raise when none exists."""

        await self._get_existing_consultation(consultation_id)
        recommendation = await self._recommendation_repository.get_by_consultation_id(
            consultation_id
        )
        if recommendation is None:
            raise ResourceNotFoundError
        return recommendation

    async def _get_existing_consultation(self, consultation_id: UUID) -> None:
        if await self._consultation_repository.get_by_id(consultation_id) is None:
            raise ResourceNotFoundError

    @staticmethod
    def _treatment_snapshot(treatment: Treatment, *, priority: int) -> dict[str, object]:
        return {
            "treatment_id": str(treatment.id),
            "name": treatment.name,
            "specialty": treatment.specialty,
            "description": treatment.description,
            "price": str(treatment.price) if treatment.price is not None else None,
            "price_min": str(treatment.price_min) if treatment.price_min is not None else None,
            "price_max": str(treatment.price_max) if treatment.price_max is not None else None,
            "duration_minutes": treatment.duration_minutes,
            "location": treatment.location,
            "default_target_area": treatment.default_target_area,
            "priority": priority,
        }
