"""Creating post table

Revision ID: 5713067a0fd9
Revises: 
Create Date: 2022-12-01 17:26:41.110722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5713067a0fd9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
