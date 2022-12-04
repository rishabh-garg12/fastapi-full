"""Add new col content

Revision ID: b7a5274ec69f
Revises: 5713067a0fd9
Create Date: 2022-12-01 18:27:39.241026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7a5274ec69f'
down_revision = '5713067a0fd9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'contheadent')
    pass
