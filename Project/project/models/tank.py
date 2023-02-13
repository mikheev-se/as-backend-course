from itertools import product
from project.models.base import Base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Tank(Base):
    __tablename__ = 'tanks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    max_capacity = Column(Float)
    current_capacity = Column(Float)
    product_id = Column(Integer,
                        ForeignKey('products.id', name='created_by_fk'))
    product = relationship('Product')
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
