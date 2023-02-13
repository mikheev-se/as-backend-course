from project.models.base import Base
from sqlalchemy import Column, Integer, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    mass = Column(Float)
    date_start = Column(TIMESTAMP(timezone=True))
    date_end = Column(TIMESTAMP(timezone=True))
    tank_id = Column(Integer, ForeignKey('tanks.id'), index=True)
    tank = relationship('Tank')
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
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
