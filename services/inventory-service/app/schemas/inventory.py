from pydantic import BaseModel, Field

class InventoryBase(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    reserved: int = Field(..., ge=0)

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: int | None = Field(None, ge=0)
    reserved: int | None = Field(None, ge=0)

class InventoryRead(InventoryBase):
    id: int

    class Config:
        from_attributes = True
