"""Create treatment catalog and link appointments.

Revision ID: 0006_create_treatments
Revises: 0005_update_recommendations_and_appointments
Create Date: 2026-08-17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006_create_treatments"
down_revision: str | Sequence[str] | None = "0005_update_recommendations_and_appointments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    treatments = op.create_table(
        "treatments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=True),
        sa.Column("price_min", sa.Numeric(10, 2), nullable=True),
        sa.Column("price_max", sa.Numeric(10, 2), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("default_target_area", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "char_length(trim(name)) > 0", name="ck_treatments_name_not_empty"
        ),
        sa.CheckConstraint(
            "char_length(trim(description)) > 0",
            name="ck_treatments_description_not_empty",
        ),
        sa.CheckConstraint("price IS NULL OR price >= 0", name="ck_treatments_price_nonnegative"),
        sa.CheckConstraint(
            "price_min IS NULL OR price_min >= 0",
            name="ck_treatments_price_min_nonnegative",
        ),
        sa.CheckConstraint(
            "price_max IS NULL OR price_max >= 0",
            name="ck_treatments_price_max_nonnegative",
        ),
        sa.CheckConstraint(
            "price_min IS NULL OR price_max IS NULL OR price_min <= price_max",
            name="ck_treatments_price_range_ordered",
        ),
        sa.CheckConstraint(
            "duration_minutes IS NULL OR duration_minutes > 0",
            name="ck_treatments_duration_positive",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_treatments_name", "treatments", ["name"], unique=True)

    op.bulk_insert(
        treatments,
        [
            {
                "id": "11111111-1111-4111-8111-111111111111",
                "name": "Dermal Fillers",
                "description": (
                    "Targeted hyaluronic acid injections to address nasolabial folds and "
                    "restore mid-face volume, directly addressing fine lines and structural "
                    "support."
                ),
                "price": 850.00,
                "price_min": 600.00,
                "price_max": 1200.00,
                "duration_minutes": 45,
                "location": "Downtown Medical Center (Primary)",
                "default_target_area": "Nasolabial Folds",
            },
            {
                "id": "22222222-2222-4222-8222-222222222222",
                "name": "Laser Resurfacing",
                "description": (
                    "Fractional non-ablative laser therapy to improve overall skin texture, "
                    "stimulate collagen production, and address mild uneven pigmentation over "
                    "3–4 sessions."
                ),
                "price": None,
                "price_min": 400.00,
                "price_max": 800.00,
                "duration_minutes": None,
                "location": None,
                "default_target_area": None,
            },
        ],
    )

    op.add_column(
        "appointments",
        sa.Column("treatment_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_appointments_treatment_id_treatments",
        "appointments",
        "treatments",
        ["treatment_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_index("ix_appointments_treatment_id", "appointments", ["treatment_id"])
    op.execute(
        """
        UPDATE appointments AS appointment
        SET treatment_id = treatment.id
        FROM treatments AS treatment
        WHERE lower(trim(appointment.treatment)) = lower(treatment.name)
        """
    )


def downgrade() -> None:
    op.drop_index("ix_appointments_treatment_id", table_name="appointments")
    op.drop_constraint(
        "fk_appointments_treatment_id_treatments",
        "appointments",
        type_="foreignkey",
    )
    op.drop_column("appointments", "treatment_id")
    op.drop_index("ix_treatments_name", table_name="treatments")
    op.drop_table("treatments")
