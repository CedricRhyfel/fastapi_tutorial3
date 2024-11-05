"""add foreign key to posts table

Revision ID: 1efd69e3787b
Revises: 321ca0100631
Create Date: 2024-11-03 23:31:30.687607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1efd69e3787b'
down_revision: Union[str, None] = '321ca0100631'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fk',
                           source_table='posts',
                           referent_table='users',
                           local_cols=['owner_id'],
                           remote_cols=['id'],
                           ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk')
    op.drop_column('posts', 'owner_id')
    pass
