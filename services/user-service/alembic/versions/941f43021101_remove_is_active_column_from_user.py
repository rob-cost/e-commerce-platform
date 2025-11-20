"""remove is_active column from user

Revision ID: 941f43021101
Revises: 46d182601fdf
Create Date: 2025-11-20 15:52:17.616756

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '941f43021101'
down_revision = '46d182601fdf'
branch_labels = None
depends_on = None

def upgrade():
     op.drop_column('users', 'is_active')


def downgrade():
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    