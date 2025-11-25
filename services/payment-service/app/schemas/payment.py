# app/schemas/payment.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum


class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class PaymentBase(BaseModel):
    order_id: int
    amount: Decimal
    provider: Optional[str] = Field(default="mock", max_length=50)


class PaymentCreate(PaymentBase):
    pass


class PaymentStatusUpdate(BaseModel):
    """
    Only status change is allowed through public endpoints (and webhook).
    """
    status: PaymentStatus


class PaymentRead(PaymentBase):
    id: int
    status: PaymentStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
