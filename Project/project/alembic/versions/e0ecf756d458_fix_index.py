"""fix: index

Revision ID: e0ecf756d458
Revises: ab906cd65c01
Create Date: 2023-03-14 11:37:34.224265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0ecf756d458'
down_revision = 'ab906cd65c01'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_users_created_by'), 'users', ['created_by'], unique=False)
    op.create_index(op.f('ix_users_updated_by'), 'users', ['updated_by'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_updated_by'), table_name='users')
    op.drop_index(op.f('ix_users_created_by'), table_name='users')
    # ### end Alembic commands ###
