"""add content column to posts table

Revision ID: c09ba672fa13
Revises: 2e8c9050f292
Create Date: 2024-11-03 00:37:32.954559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c09ba672fa13'
down_revision: Union[str, None] = '2e8c9050f292'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass