"""Added a view_count column to blog_posts

Revision ID: 5f7bbd981d01
Revises: 968e983a31fd
Create Date: 2024-07-19 10:41:48.880077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f7bbd981d01'
down_revision: Union[str, None] = '968e983a31fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog_posts', sa.Column('view_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blog_posts', 'view_count')
    # ### end Alembic commands ###
