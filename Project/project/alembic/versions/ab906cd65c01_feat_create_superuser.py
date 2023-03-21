"""feat: create superuser

Revision ID: ab906cd65c01
Revises: f2a5ea7dd3e2
Create Date: 2023-03-13 18:33:11.205549

"""
from alembic import op
import sqlalchemy as sa
from project.core.settings import settings
from project.entities.user_entity import User
from project.service.jwt_service import JwtService


# revision identifiers, used by Alembic.
revision = 'ab906cd65c01'
down_revision = 'f2a5ea7dd3e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    admin = {
        'username': f"'{settings.username}'",
        'password_hashed': f"'{JwtService.hash_password(settings.password)}'",
        'role': "'admin'"
    }
    create_superuser_query = f'insert into {User.__tablename__} ({", ".join(list(admin.keys()))}) values ({", ".join(list(admin.values()))})'
    op.execute(create_superuser_query)


def downgrade() -> None:
    admin = {
        'username': f"'{settings.username}'",
    }
    delete_superuser_query = f'delete from {User.__tablename__} where {", ".join(list(admin.keys()))} = {", ".join(list(admin.values()))}'
    op.execute(delete_superuser_query)
