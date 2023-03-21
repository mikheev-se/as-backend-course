from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from project.entities.base import Base
from typing import Literal, get_args

valid_roles = Literal['admin', 'viewer']
roles = get_args(valid_roles)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hashed = Column(String)
    role = Column(Enum(*roles, name='ct_roles'), default='viewer')
    created_by = Column(Integer, ForeignKey('users.id'),
                        index=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default=func.now())
    creator = relationship('User', foreign_keys=[
                           created_by],
                           remote_side=[id],
                           post_update=True)
    updated_by = Column(Integer, ForeignKey('users.id'),
                        index=True)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=func.now(),
                        onupdate=func.now())
    updater = relationship('User', foreign_keys=[
                           updated_by],
                           remote_side=[id],
                           post_update=True)
