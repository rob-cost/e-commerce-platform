from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.order import Order, OrderStatus
from app.models.orderItem import OrderItem
from app.schemas.order import OrderCreate, OrderStatusUpdate

class OrderNotFoundError(Exception):
    pass

class InvalidOrderStatusTransition(Exception):
    pass


def create_order(db: Session, order_data: OrderCreate) -> Order:
    # Create a new order
    order = Order(
        user_id=order_data.user_id,
        total_amount=Decimal("0.00"),
        status=OrderStatus.pending,
    )
    db.add(order)
    db.flush()  # send insert to db and so order.id is available

    total = Decimal("0.00")

    for item_data in order_data.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data.product_id,
            price=item_data.price,        # you store snapshot price from request
            quantity=item_data.quantity,
        )
        db.add(order_item)

        total += item_data.price * item_data.quantity

    order.total_amount = total

    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise OrderNotFoundError(f"Order {order_id} not found")
    return order

def list_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


ALLOWED_TRANSITIONS = {
    "pending": {"paid", "cancelled"},
    "paid": {"cancelled"},
    "cancelled": set()
}

def update_order_status(db: Session, order_id: int, update: OrderStatusUpdate) -> Order:
    order = get_order(db, order_id)

    current = order.status.value
    new = update.status.value

    allowed = ALLOWED_TRANSITIONS.get(current, set())

    if new not in allowed:
        # idempotent (same → same)
        if new == current:
            return order
        raise InvalidOrderStatusTransition(f"Cannot change {current} → {new}")

    order.status = new

    db.commit()
    db.refresh(order)
    return order


def cancel_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if order.status == OrderStatus.paid:
        raise ValueError(f"Cannot cancel a paid order")
    
    order.status = OrderStatus.cancelled
    db.commit()
    db.refresh(order)
    return order
