"""Update recommendation treatment structure and timestamps.

Revision ID: 0005_update_recommendations_and_appointments
Revises: 0004_create_appointments
Create Date: 2026-08-13
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0005_update_recommendations_and_appointments"
down_revision: str | Sequence[str] | None = "0004_create_appointments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "recommendations",
        "recommended_treatment",
        new_column_name="recommended_treatments",
    )
    op.alter_column(
        "recommendations",
        "recommended_treatments",
        type_=postgresql.JSONB(),
        postgresql_using=(
            "jsonb_build_array(jsonb_build_object("
            "'name', recommended_treatments, "
            "'description', 'Migrated from legacy recommended_treatment.'))"
        ),
    )
    for table_name in ("recommendations", "appointments"):
        op.add_column(
            table_name,
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            ),
        )


def downgrade() -> None:
    op.drop_column("appointments", "updated_at")
    op.drop_column("recommendations", "updated_at")
    op.alter_column(
        "recommendations",
        "recommended_treatments",
        type_=sa.Text(),
        postgresql_using="recommended_treatments->0->>'name'",
    )
    op.alter_column(
        "recommendations",
        "recommended_treatments",
        new_column_name="recommended_treatment",
    )
