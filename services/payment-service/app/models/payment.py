# services/payment-service/app/models/payment.py
from sqlalchemy import Column, Integer, String, DECIMAL, Enum, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class PaymentStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)  # references Order.id
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    provider = Column(String(50), default="mock")  # stripe, paypal, mock
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
