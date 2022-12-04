"""Adding foreign key to post table

Revision ID: 62ffd3f50509
Revises: 7ce637e00d68
Create Date: 2022-12-01 23:19:14.153667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62ffd3f50509'
down_revision = '7ce637e00d68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
