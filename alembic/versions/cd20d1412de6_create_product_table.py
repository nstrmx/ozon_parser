"""create product table

Revision ID: cd20d1412de6
Revises: 
Create Date: 2023-10-22 02:01:33.436095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd20d1412de6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'product',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Unicode(200), nullable=False),
        sa.Column('old_price', sa.Integer, nullable=False),
        sa.Column('new_price', sa.Integer, nullable=False),
        sa.Column('discount', sa.Integer, nullable=False),
    )
    op.add_column('product', sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False))


def downgrade() -> None:
    op.drop_table('product')
