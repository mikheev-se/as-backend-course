"""fix: remove default values since they don't work

Revision ID: abd53c807df4
Revises: 5aad35d5d963
Create Date: 2023-02-12 20:51:52.438883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abd53c807df4'
down_revision = '5aad35d5d963'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
