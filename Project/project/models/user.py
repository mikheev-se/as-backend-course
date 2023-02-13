from project.models.base import Base
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hashed = Column(String)
    role = Column(Enum('admin', 'viewer', name='ct_roles'), default='viewer')
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    created_by = Column(Integer,
                        ForeignKey('users.id', name='created_by_fk'),
                        index=True)
    creator = relationship('User', foreign_keys=[
                           created_by],
                           remote_side=[id],)
    modified_at = Column(TIMESTAMP(timezone=True),
                         default=func.now(),
                         onupdate=func.now())
    modified_by = Column(Integer,
                         ForeignKey('users.id', name='updated_by_fk'),
                         index=True)
    modifier = relationship('User', foreign_keys=[
                            modified_by],
                            remote_side=[id])
