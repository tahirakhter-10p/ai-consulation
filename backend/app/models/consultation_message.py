from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Text
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel
from app.models.enums import MessageRole

if TYPE_CHECKING:
    from app.models.consultation import Consultation


class ConsultationMessage(BaseModel):
    """A persisted user or AI message belonging to one consultation."""

    __tablename__ = "consultation_messages"
    __table_args__ = (
        CheckConstraint(
            "char_length(trim(content)) > 0", name="ck_consultation_messages_content_not_empty"
        ),
    )

    consultation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("consultations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[MessageRole] = mapped_column(
        SQLAlchemyEnum(
            MessageRole,
            name="message_role",
            values_callable=lambda enum: [member.value for member in enum],
        ),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    consultation: Mapped[Consultation] = relationship(back_populates="messages")
