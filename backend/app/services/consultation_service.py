from dataclasses import dataclass
from uuid import UUID

from app.ai.schemas.chat import AIChatMessage
from app.ai.service import AIService
from app.core.exceptions import InvalidOperationError, ResourceNotFoundError
from app.models.consultation import Consultation
from app.models.consultation_message import ConsultationMessage
from app.models.enums import ConsultationStatus, MessageRole
from app.repositories.consultation_repository import ConsultationRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.recommendation_repository import RecommendationRepository


@dataclass(frozen=True)
class ConsultationListRecord:
    """A consultation paired with the procedure currently recommended for it."""

    consultation: Consultation
    recommended_procedure: str


class ConsultationService:
    """Coordinate the consultation record and persisted chat workflows."""

    def __init__(
        self,
        consultation_repository: ConsultationRepository,
        message_repository: MessageRepository,
        recommendation_repository: RecommendationRepository,
        ai_service: AIService,
    ) -> None:
        self._consultation_repository = consultation_repository
        self._message_repository = message_repository
        self._recommendation_repository = recommendation_repository
        self._ai_service = ai_service

    async def create_consultation(self, *, patient_name: str, primary_concern: str) -> Consultation:
        """Create a pending consultation after normalizing required text fields."""

        return await self._consultation_repository.create(
            patient_name=self._required_text(patient_name, field_name="patient_name"),
            primary_concern=self._required_text(primary_concern, field_name="primary_concern"),
        )

    async def get_consultation(self, consultation_id: UUID) -> Consultation:
        """Return a consultation or raise when the identifier does not exist."""

        consultation = await self._consultation_repository.get_by_id(consultation_id)
        if consultation is None:
            raise ResourceNotFoundError
        return consultation

    async def list_consultations(
        self,
        *,
        search: str | None = None,
        status: ConsultationStatus | None = None,
    ) -> list[Consultation]:
        """List consultations with the repository's optional search and status filters."""

        normalized_search = search.strip() if search is not None else None
        return await self._consultation_repository.list(
            search=normalized_search or None,
            status=status,
        )

    async def list_consultation_records(
        self,
        *,
        search: str | None = None,
        status: ConsultationStatus | None = None,
    ) -> list[ConsultationListRecord]:
        """Return consultations with their stored treatment or the pending placeholder."""

        consultations = await self.list_consultations(search=search, status=status)
        records: list[ConsultationListRecord] = []
        for consultation in consultations:
            recommendation = await self._recommendation_repository.get_by_consultation_id(
                consultation.id
            )
            records.append(
                ConsultationListRecord(
                    consultation=consultation,
                    recommended_procedure=(
                        recommendation.recommended_treatments[0]["name"]
                        if recommendation
                        else "Pending"
                    ),
                )
            )
        return records

    async def update_status(
        self, consultation_id: UUID, status: ConsultationStatus
    ) -> Consultation:
        """Update and return an existing consultation's lifecycle status."""

        consultation = await self._consultation_repository.update_status(consultation_id, status)
        if consultation is None:
            raise ResourceNotFoundError
        return consultation

    async def get_conversation(self, consultation_id: UUID) -> list[ConsultationMessage]:
        """Return chronological chat history for an existing consultation."""

        await self.get_consultation(consultation_id)
        return await self._message_repository.get_conversation(consultation_id)

    async def send_message(
        self,
        *,
        consultation_id: UUID,
        message: str,
    ) -> tuple[ConsultationMessage, ConsultationMessage]:
        """Persist a user message, generate an AI reply, and persist that reply."""

        await self.get_consultation(consultation_id)
        user_message = await self._message_repository.save(
            consultation_id=consultation_id,
            role=MessageRole.USER,
            content=self._required_text(message, field_name="message"),
        )
        conversation = await self._message_repository.get_conversation(consultation_id)
        ai_response = await self._ai_service.generate_chat_response(
            [
                AIChatMessage(role=message.role.value, content=message.content)
                for message in conversation
            ]
        )
        response = await self._message_repository.save(
            consultation_id=consultation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response.content,
        )
        return user_message, response

    @staticmethod
    def _required_text(value: str, *, field_name: str) -> str:
        if not isinstance(value, str) or not (normalized_value := value.strip()):
            raise InvalidOperationError
        return normalized_value
