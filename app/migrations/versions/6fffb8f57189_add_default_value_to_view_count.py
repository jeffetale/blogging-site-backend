"""Add default value to view_count

Revision ID: 6fffb8f57189
Revises: 5f7bbd981d01
Create Date: 2024-07-19 11:49:30.896602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fffb8f57189'
down_revision: Union[str, None] = '5f7bbd981d01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.alter_column('blog_posts', 'view_count', server_default='0')
    pass

def downgrade() -> None:
    # op.alter_column('blog_posts', 'view_count', server_default=None)
    pass

