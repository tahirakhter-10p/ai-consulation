"""Add treatment specialty and lifecycle status.

Revision ID: 0007_expand_treatment_catalog
Revises: 0006_create_treatments
Create Date: 2026-08-17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0007_expand_treatment_catalog"
down_revision: str | Sequence[str] | None = "0006_create_treatments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("treatments", sa.Column("specialty", sa.String(length=120), nullable=True))
    op.add_column(
        "treatments",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.execute("UPDATE treatments SET specialty = 'Dermatology' WHERE specialty IS NULL")
    op.alter_column("treatments", "specialty", nullable=False)
    op.create_check_constraint(
        "ck_treatments_specialty_not_empty",
        "treatments",
        "char_length(trim(specialty)) > 0",
    )
    op.create_index("ix_treatments_specialty", "treatments", ["specialty"])
    op.create_index("ix_treatments_is_active", "treatments", ["is_active"])


def downgrade() -> None:
    op.drop_index("ix_treatments_is_active", table_name="treatments")
    op.drop_index("ix_treatments_specialty", table_name="treatments")
    op.drop_constraint(
        "ck_treatments_specialty_not_empty", "treatments", type_="check"
    )
    op.drop_column("treatments", "is_active")
    op.drop_column("treatments", "specialty")
