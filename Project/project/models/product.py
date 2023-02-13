from project.models.base import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    created_by = Column(Integer,
                        ForeignKey('users.id', name='created_by_fk'),
                        index=True)
    creator = relationship('User', foreign_keys=[created_by])
    modified_at = Column(TIMESTAMP(timezone=True),
                         default=func.now(),
                         onupdate=func.now())
    modified_by = Column(Integer,
                         ForeignKey('users.id', name='updated_by_fk'),
                         index=True)
    modifier = relationship('User', foreign_keys=[modified_by])
