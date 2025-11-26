from pydantic import BaseModel
from decimal import Decimal

class OrderItemBase(BaseModel):
    product_id: int
    price: Decimal
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True
