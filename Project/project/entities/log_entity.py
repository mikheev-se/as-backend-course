from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from project.entities.base import Base
from typing import Literal, get_args

valid_actions = Literal['prepare', 'fit', 'predict',
                        'download']
actions = get_args(valid_actions)


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    action = Column(Enum(*actions, name='ct_actions'))
    invoked_by = Column(Integer, ForeignKey('users.id'))
    invoked_at = Column(TIMESTAMP(timezone=True),
                        default=func.now())
    invoker = relationship('User', foreign_keys=[
                           invoked_by])
