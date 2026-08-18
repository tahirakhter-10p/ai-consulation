"""Create consultations table.

Revision ID: 0001_create_consultations
Revises:
Create Date: 2026-08-05
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_create_consultations"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Alembic creates this table before applying the initial revision. Later
    # revision identifiers exceed its default VARCHAR(32) width.
    op.alter_column(
        "alembic_version",
        "version_num",
        existing_type=sa.String(length=32),
        type_=sa.String(length=64),
        existing_nullable=False,
    )
    consultation_status = postgresql.ENUM(
        "Pending", "Booked", "Completed", name="consultation_status", create_type=False
    )
    consultation_status.create(op.get_bind(), checkfirst=False)
    op.create_table(
        "consultations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_name", sa.String(length=255), nullable=False),
        sa.Column("primary_concern", sa.Text(), nullable=False),
        sa.Column("status", consultation_status, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "char_length(trim(patient_name)) > 0", name="ck_consultations_patient_name_not_empty"
        ),
        sa.CheckConstraint(
            "char_length(trim(primary_concern)) > 0",
            name="ck_consultations_primary_concern_not_empty",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_consultations_patient_name", "consultations", ["patient_name"], unique=False
    )
    op.create_index("ix_consultations_status", "consultations", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_consultations_status", table_name="consultations")
    op.drop_index("ix_consultations_patient_name", table_name="consultations")
    op.drop_table("consultations")
    postgresql.ENUM(name="consultation_status").drop(op.get_bind(), checkfirst=False)
