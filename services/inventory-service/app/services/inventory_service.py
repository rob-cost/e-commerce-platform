from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate

class InventoryItemNotFound(Exception):
    pass

class InventoryAlreadyExist(Exception):
    pass

class QuantityAndReserveNegative(Exception):
    pass

class ReservedAmountExceeded(Exception):
    pass

class QuantityAmountExceeded(Exception):
    pass

class LowInStock(Exception):
    pass


def get_inventory(db: Session, inventory_id: int):
    inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inv:
        raise InventoryItemNotFound(f"Inventory Item Not Found")
    return inv


def get_inventory_by_product(db: Session, product_id: int):
    return db.query(Inventory).filter(Inventory.product_id == product_id).first()



def list_inventory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Inventory).offset(skip).limit(limit).all()


def create_inventory(db: Session, data: InventoryCreate):
    existing = get_inventory_by_product(db, data.product_id)
    if existing:
        raise InventoryAlreadyExist(f"Inventory for this product already exists")

    inv = Inventory(**data.model_dump())
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv


def update_inventory(db: Session, inventory_id: int, data: InventoryUpdate):
    inv = get_inventory(db, inventory_id)

    ALLOW_FIELDS = {"quantity", "reserved"}
    for field, value in data.model_dump(exclude_unset= True).items():
        if field in ALLOW_FIELDS:
            setattr(inv, field, value)
    
    if inv.quantity < 0 or inv.reserved < 0:
        raise QuantityAndReserveNegative(f"quantity and reserved must be >= 0")
    if inv.reserved > inv.quantity:
        raise ReservedAmountExceeded(f"reserved cannot exceed quantity")
    
    db.commit()
    db.refresh(inv)
    return inv


def delete_inventory(db: Session, inventory_id: int):
    inv = get_inventory(db, inventory_id)
    db.delete(inv)
    db.commit()
    return {"message": "Inventory deleted"}


def reserve_stock(db: Session, product_id: int, quantity: int):
    inv = get_inventory_by_product(db, product_id)

    available = inv.quantity - inv.reserved
    if available < quantity:
        raise LowInStock(f"Not enough stock available")

    inv.reserved += quantity
    db.commit()
    db.refresh(inv)
    return inv


def confirm_stock(db: Session, product_id: int, quantity: int):
    inv = get_inventory_by_product(db, product_id)

    if inv.reserved < quantity:
        raise ReservedAmountExceeded(f"Cannot confirm more stock than reserved")

    inv.reserved -= quantity
    inv.quantity -= quantity

    db.commit()
    db.refresh(inv)
    return inv


def release_stock(db: Session, product_id: int, quantity: int):
    inv = get_inventory_by_product(db, product_id)

    if inv.reserved < quantity:
        raise ReservedAmountExceeded(f"Cannot release more than reserved")

    inv.reserved -= quantity
    db.commit()
    db.refresh(inv)
    return inv
