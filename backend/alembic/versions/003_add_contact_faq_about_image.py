"""add contact fields, about_image_url, and FAQ table

Revision ID: 003
Revises: 002
Create Date: 2026-07-27

Adiciona:
- tenants: address, phone, email, whatsapp, map_embed_url
- site_content: about_image_url
- site_faq: nova tabela (id, tenant_id, question, answer, sort_order)
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---- tenants: add contact/location columns ----
    op.add_column("tenants", sa.Column("address", sa.Text(), nullable=True))
    op.add_column("tenants", sa.Column("phone", sa.String(30), nullable=True))
    op.add_column("tenants", sa.Column("email", sa.String(255), nullable=True))
    op.add_column("tenants", sa.Column("whatsapp", sa.String(30), nullable=True))
    op.add_column("tenants", sa.Column("map_embed_url", sa.Text(), nullable=True))

    # ---- site_content: add about_image_url ----
    op.add_column("site_content", sa.Column("about_image_url", sa.Text(), nullable=True))

    # ---- site_faq: new table ----
    op.create_table(
        "site_faq",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("question", sa.String(500), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False, server_default=""),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("site_faq")
    op.drop_column("site_content", "about_image_url")
    op.drop_column("tenants", "map_embed_url")
    op.drop_column("tenants", "whatsapp")
    op.drop_column("tenants", "email")
    op.drop_column("tenants", "phone")
    op.drop_column("tenants", "address")
