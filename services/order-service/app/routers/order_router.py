from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.order import OrderRead, OrderCreate, OrderStatusUpdate
from app.services.order_service import (
    OrderNotFoundError,
    InvalidOrderStatusTransition,
    get_order,
    list_orders,
    create_order,
    update_order_status,
    cancel_order
)
from app.database import get_db

router = APIRouter()

@router.get("/orders/{order_id}", response_model=OrderRead)
def api_get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        return get_order(db, order_id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    
@router.get("/orders", response_model=List[OrderRead])
def api_list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_orders(db, skip, limit)

@router.post("/orders", response_model=OrderRead, status_code=201)
def api_create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)

    
@router.patch("/orders/{order_id}/status", response_model=OrderRead)
def api_update_status(order_id: int, update: OrderStatusUpdate, db: Session = Depends(get_db)):
    try:
        return update_order_status(db, order_id, update)
    except OrderNotFoundError:
        raise HTTPException(404, "Order not found")
    except InvalidOrderStatusTransition as e:
        raise HTTPException(400, str(e))
    
@router.put("\orders\{order_id}")
def api_cancel_order(order_id: int, db: Session = Depends(get_db)):
    try:
        return cancel_order(db, order_id)
    except OrderNotFoundError:
        raise HTTPException(404, "Order not found")
    except Exception as e:
        raise HTTPException(status_code=505, detail=str(e))
    