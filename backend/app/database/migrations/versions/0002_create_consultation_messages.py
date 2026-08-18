"""Create consultation messages table.

Revision ID: 0002_create_consultation_messages
Revises: 0001_create_consultations
Create Date: 2026-08-05
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_create_consultation_messages"
down_revision: str | Sequence[str] | None = "0001_create_consultations"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    message_role = postgresql.ENUM("user", "assistant", name="message_role", create_type=False)
    message_role.create(op.get_bind(), checkfirst=False)
    op.create_table(
        "consultation_messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("consultation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", message_role, nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "char_length(trim(content)) > 0", name="ck_consultation_messages_content_not_empty"
        ),
        sa.ForeignKeyConstraint(["consultation_id"], ["consultations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_consultation_messages_consultation_id",
        "consultation_messages",
        ["consultation_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_consultation_messages_consultation_id", table_name="consultation_messages")
    op.drop_table("consultation_messages")
    postgresql.ENUM(name="message_role").drop(op.get_bind(), checkfirst=False)
