from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consultation_message import ConsultationMessage
from app.models.enums import MessageRole


class MessageRepository:
    """Persist and retrieve consultation conversation messages."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(
        self,
        *,
        consultation_id: UUID,
        role: MessageRole,
        content: str,
    ) -> ConsultationMessage:
        """Add a message to the current unit of work and return it."""

        message = ConsultationMessage(
            consultation_id=consultation_id,
            role=role,
            content=content,
        )
        self._session.add(message)
        await self._session.flush()
        await self._session.refresh(message)
        return message

    async def get_conversation(self, consultation_id: UUID) -> list[ConsultationMessage]:
        """Return a consultation's messages in chronological order."""

        statement = (
            select(ConsultationMessage)
            .where(ConsultationMessage.consultation_id == consultation_id)
            .order_by(ConsultationMessage.created_at.asc())
        )
        result = await self._session.scalars(statement)
        return list(result.all())
