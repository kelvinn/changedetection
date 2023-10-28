"""create price table

Revision ID: a908654d79a3
Revises: 669504a609e1
Create Date: 2023-10-28 12:59:44.307668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a908654d79a3'
down_revision: Union[str, None] = '669504a609e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'prices',
        sa.Column('gid', sa.Integer, primary_key=True),
        sa.Column('amount', sa.Float(10), nullable=False),
        sa.Column('product_gid', sa.Integer, sa.ForeignKey('products.gid')),
        sa.Column('created', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('prices')

