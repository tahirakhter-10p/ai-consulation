from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.consultation import Consultation


class Recommendation(BaseModel):
    """The single generated clinical recommendation for a consultation."""

    __tablename__ = "recommendations"

    consultation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("consultations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    patient_summary: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_treatments: Mapped[list[dict[str, object]]] = mapped_column(JSONB, nullable=False)
    ai_reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    consultation: Mapped[Consultation] = relationship(back_populates="recommendation")
