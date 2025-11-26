# services/order-service/app/models/order_item.py
from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from app.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)  # references Order.id
    product_id = Column(Integer, nullable=False)  # snapshot of Product.id
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
