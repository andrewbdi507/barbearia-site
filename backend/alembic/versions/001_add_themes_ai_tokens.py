"""add themes, ai_tokens, max_concurrent_users to plans

Revision ID: 001
Revises: None
Create Date: 2026-07-22

This is the first migration. It adds columns that exist in the SQLAlchemy model
but were never created in the database (no migrations existed before).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add themes column (JSONB, NOT NULL, default empty array)
    op.add_column(
        "plans",
        sa.Column(
            "themes",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )

    # Add ai_tokens column (Integer, nullable — null means unlimited)
    op.add_column(
        "plans",
        sa.Column("ai_tokens", sa.Integer(), nullable=True),
    )

    # Add max_concurrent_users column (Integer, nullable — null means unlimited)
    op.add_column(
        "plans",
        sa.Column("max_concurrent_users", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("plans", "max_concurrent_users")
    op.drop_column("plans", "ai_tokens")
    op.drop_column("plans", "themes")
