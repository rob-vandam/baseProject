"""create user table

Revision ID: 0d069b2154b5
Revises: 
Create Date: 2023-07-13 12:38:28.579211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d069b2154b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('authtoken', sa.String(), nullable=False),
        sa.Column('idtoken', sa.String(), nullable=True),
        sa.Column('refreshtoken', sa.String(), nullable=True),
        sa.Column('admin_id', sa.Integer, nullable=False),
        sa.Column('app_id', sa.Integer, nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('lang', sa.String(), nullable=False),
        sa.Column('chain_id', sa.Integer, nullable=True),
        )



def downgrade() -> None:
    op.drop_table('users')
