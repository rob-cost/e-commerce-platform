from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class ProductBase(BaseModel):
    seller_id: int
    title: str
    description: Optional[str]
    image_url: Optional[str]
    price: float = Field(gt=0)


class ProductRead(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass

    class Config:
        orm_mode = True
 

class ProductUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    price: Optional[float]