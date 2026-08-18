"""Create recommendations table.

Revision ID: 0003_create_recommendations
Revises: 0002_create_consultation_messages
Create Date: 2026-08-05
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003_create_recommendations"
down_revision: str | Sequence[str] | None = "0002_create_consultation_messages"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("consultation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_summary", sa.Text(), nullable=False),
        sa.Column("recommended_treatment", sa.Text(), nullable=False),
        sa.Column("ai_reasoning", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["consultation_id"], ["consultations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("consultation_id"),
    )


def downgrade() -> None:
    op.drop_table("recommendations")
