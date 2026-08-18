from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, String, Text, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel
from app.models.enums import ConsultationStatus

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.consultation_message import ConsultationMessage
    from app.models.recommendation import Recommendation


class Consultation(BaseModel):
    """A patient's consultation session and its related workflow records."""

    __tablename__ = "consultations"
    __table_args__ = (
        CheckConstraint(
            "char_length(trim(patient_name)) > 0", name="ck_consultations_patient_name_not_empty"
        ),
        CheckConstraint(
            "char_length(trim(primary_concern)) > 0",
            name="ck_consultations_primary_concern_not_empty",
        ),
    )

    patient_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    primary_concern: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ConsultationStatus] = mapped_column(
        SQLAlchemyEnum(
            ConsultationStatus,
            name="consultation_status",
            values_callable=lambda enum: [member.value for member in enum],
        ),
        nullable=False,
        index=True,
        default=ConsultationStatus.PENDING,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    messages: Mapped[list[ConsultationMessage]] = relationship(
        back_populates="consultation", cascade="all, delete-orphan", passive_deletes=True
    )
    recommendation: Mapped[Recommendation | None] = relationship(
        back_populates="consultation",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False,
    )
    appointment: Mapped[Appointment | None] = relationship(
        back_populates="consultation",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False,
    )
