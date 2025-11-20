"""add payments index for order 

Revision ID: 734915830060
Revises: fc305a34be1e
Create Date: 2025-11-20 10:23:26.916819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '734915830060'
down_revision: Union[str, None] = 'fc305a34be1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_payments_order_id', 'payments', ['order_id'])


def downgrade() -> None:
    op.drop_index('ix_payments_order_id', table_name='payments')