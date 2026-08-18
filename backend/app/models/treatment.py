from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.appointment import Appointment


class Treatment(BaseModel):
    """Authoritative treatment metadata available to recommendation and booking workflows."""

    __tablename__ = "treatments"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="ck_treatments_name_not_empty"),
        CheckConstraint(
            "char_length(trim(description)) > 0",
            name="ck_treatments_description_not_empty",
        ),
        CheckConstraint(
            "char_length(trim(specialty)) > 0", name="ck_treatments_specialty_not_empty"
        ),
        CheckConstraint("price IS NULL OR price >= 0", name="ck_treatments_price_nonnegative"),
        CheckConstraint(
            "price_min IS NULL OR price_min >= 0",
            name="ck_treatments_price_min_nonnegative",
        ),
        CheckConstraint(
            "price_max IS NULL OR price_max >= 0",
            name="ck_treatments_price_max_nonnegative",
        ),
        CheckConstraint(
            "price_min IS NULL OR price_max IS NULL OR price_min <= price_max",
            name="ck_treatments_price_range_ordered",
        ),
        CheckConstraint(
            "duration_minutes IS NULL OR duration_minutes > 0",
            name="ck_treatments_duration_positive",
        ),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    specialty: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    price_min: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    price_max: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    default_target_area: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true", index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    appointments: Mapped[list[Appointment]] = relationship(back_populates="treatment_record")
