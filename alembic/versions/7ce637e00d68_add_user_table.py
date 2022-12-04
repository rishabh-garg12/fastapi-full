"""Add user table

Revision ID: 7ce637e00d68
Revises: b7a5274ec69f
Create Date: 2022-12-01 18:53:30.299094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ce637e00d68'
down_revision = 'b7a5274ec69f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # We can also make same primary or unique as in models
    op.create_table("users",
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
