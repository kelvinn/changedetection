"""create product table

Revision ID: 669504a609e1
Revises: 
Create Date: 2023-10-28 12:16:28.373213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '669504a609e1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('gid', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('url', sa.String(500), nullable=False, unique=True),
        sa.Column('created', sa.DateTime),
        sa.Column('last_updated', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('products')
