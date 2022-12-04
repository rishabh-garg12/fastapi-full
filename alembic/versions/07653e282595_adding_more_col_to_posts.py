"""Adding more col to posts

Revision ID: 07653e282595
Revises: 62ffd3f50509
Create Date: 2022-12-01 23:25:01.623986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07653e282595'
down_revision = '62ffd3f50509'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(),
                            server_default='True', nullable=False))

    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                     nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts')
    pass
