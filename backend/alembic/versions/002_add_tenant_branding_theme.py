"""add theme to tenant_branding

Revision ID: 002
Revises: 001
Create Date: 2026-07-22

Migration separada porque a 001 já havia sido aplicada em produção
antes da coluna `theme` ser adicionada ao modelo TenantBrandingModel.
Modificar a 001 sem incrementar o revision faz o Alembic pular a migração.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tenant_branding",
        sa.Column("theme", sa.String(30), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("tenant_branding", "theme")
