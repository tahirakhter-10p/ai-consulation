from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.consultation import Consultation
    from app.models.treatment import Treatment


class Appointment(BaseModel):
    """The single booked appointment resulting from a consultation."""

    __tablename__ = "appointments"

    consultation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("consultations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    treatment_id: Mapped[UUID | None] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("treatments.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    treatment: Mapped[str] = mapped_column(String(255), nullable=False)
    appointment_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    consultation: Mapped[Consultation] = relationship(back_populates="appointment")
    treatment_record: Mapped[Treatment | None] = relationship(back_populates="appointments")
