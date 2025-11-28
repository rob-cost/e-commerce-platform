from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.inventory_service import (
    list_inventory,
    get_inventory,
    create_inventory,
    update_inventory,
    delete_inventory,
    reserve_stock,
    confirm_stock,
    release_stock,
    InventoryItemNotFound,
    InventoryAlreadyExist,
    QuantityAmountExceeded,
    QuantityAndReserveNegative,
    ReservedAmountExceeded,
    LowInStock
)
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryRead

router = APIRouter()


@router.get("/inventory/", response_model=list[InventoryRead])
def api_list_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_inventory(db, skip, limit)


@router.get("/inventory/{inventory_id}", response_model=InventoryRead)
def api_get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    try:
        return get_inventory(db, inventory_id)
    except InventoryItemNotFound:
        raise HTTPException(status_code=404, detail='Inventory item not found')


@router.post("/inventory/", response_model=InventoryRead)
def api_create_inventory(data: InventoryCreate, db: Session = Depends(get_db)):
    try:
        return create_inventory(db, data)
    except InventoryAlreadyExist:
        raise HTTPException(status_code=400, detail='Inventory for this product already exists')


@router.put("/inventory/{inventory_id}", response_model=InventoryRead)
def api_update_inventory(inventory_id: int, data: InventoryUpdate, db: Session = Depends(get_db)):
    try:
        return update_inventory(db, inventory_id, data)
    except QuantityAndReserveNegative:
        raise HTTPException(status_code=400, detail="quantity and reserved must be >= 0")
    except ReservedAmountExceeded:
        raise HTTPException(status_code=400, detail="reserved cannot exceed quantity")



@router.delete("/inventory/{inventory_id}")
def api_delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    return delete_inventory(db, inventory_id)
