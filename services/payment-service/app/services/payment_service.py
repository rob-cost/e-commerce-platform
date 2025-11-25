from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from decimal import Decimal

from app.models.payment import Payment  # your SQLAlchemy model
from app.schemas.payment import PaymentCreate, PaymentStatus, PaymentStatusUpdate

class PaymentNotFoundError(Exception):
    """Raised when a payment cannot be found."""
    pass


class InvalidPaymentStatusTransition(Exception):
    """Raised when attempting an invalid status transition."""
    pass


class PaymentCreationError(Exception):
    """Raised when payment creation fails for business reasons."""
    pass


# Define allowed transitions for status
ALLOWED_TRANSITIONS = {
    "pending": {"completed", "failed"},
    "failed": {"pending"},       # if you support manual retry
    "completed": set(),          # completed is terminal
}


def create_payment(db: Session, payment_in: PaymentCreate):
    """
    Create a new payment. Status defaults to pending in the model.
    Do not allow client to set status/created_at/updated_at/id.
    """
    # Basic business validation
    if payment_in.amount <= Decimal("0.00"):
        raise PaymentCreationError("Amount must be > 0")

    payment = Payment(
        order_id=payment_in.order_id,
        amount=payment_in.amount,
        provider=payment_in.provider,
        # status intentionally left to DB default (PaymentStatus.pending)
    )

    try:
        db.add(payment)
        db.commit()
        db.refresh(payment)

        return payment
    except IntegrityError as e:
        db.rollback()
        # customize if you have unique constraints or fk constraints
        raise PaymentCreationError("Database integrity error while creating payment") from e
    except SQLAlchemyError as e:
        db.rollback()
        raise PaymentCreationError("Database error while creating payment") from e


def get_payment(db: Session, payment_id: int) -> Payment:
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise PaymentNotFoundError(f"Payment {payment_id} not found")
    return payment


def list_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Payment).offset(skip).limit(limit).all()


def list_payments_by_order(db: Session, order_id: int):
    return db.query(Payment).filter(Payment.order_id == order_id).all()


def update_payment_status(db: Session, payment_id: int, status_update: PaymentStatusUpdate) -> Payment:
    """
    Only change status. Validate allowed transitions.
    This function is used by admin endpoints or by internal code (e.g. webhook handler).
    """
    payment = get_payment(db, payment_id)  # raises if not found

    current = payment.status.value if hasattr(payment.status, "value") else payment.status
    new_status = status_update.status.value if hasattr(status_update.status, "value") else status_update.status

    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if new_status not in allowed:
        # Allow idempotent updates (same -> same) but reject invalid transitions
        if new_status == current:
            return payment
        raise InvalidPaymentStatusTransition(f"Cannot change status from {current} to {new_status}")

    payment.status = status_update.status
    try:
        db.commit()
        db.refresh(payment)
    except SQLAlchemyError:
        db.rollback()
        raise

    return payment


def mark_payment_as_cancelled(db: Session, payment_id: int):
    """
    If you need a cancellation flow, implement as a status or separate field.
    Example: treat 'failed' as cancellation, or add a 'canceled' flag in the model.
    """
    # Example: map cancel to failed
    return update_payment_status(db, payment_id, PaymentStatusUpdate(status=PaymentStatus.failed))
