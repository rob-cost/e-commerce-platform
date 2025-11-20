"""add order_items foreign key and indexes

Revision ID: 6e745e290755
Revises: a7eefa592d3f
Create Date: 2025-11-20 10:14:45.211254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e745e290755'
down_revision: Union[str, None] = 'a7eefa592d3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add foreign key from order_items.order_id → orders.id
    op.create_foreign_key(
        'fk_order_items_order',
        source_table='order_items',
        referent_table='orders',
        local_cols=['order_id'],
        remote_cols=['id']
    )


def downgrade() -> None:
    # Remove foreign key and index
    op.drop_index('ix_order_items_order_id', table_name='order_items')
    op.drop_constraint('fk_order_items_order', 'order_items', type_='foreignkey')