# create an order when a purchase is made

from sqlalchemy import Column, Integer, DECIMAL, Enum, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class OrderStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False) # refer to user id
    total_amount = Column(DECIMAL(10,2), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())