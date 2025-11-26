# app/routers/payments.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db  # db dependency
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentStatusUpdate, PaymentStatus
from app.services.payment_service import (
    create_payment,
    get_payment,
    list_payments,
    list_payments_by_order,
    update_payment_status,
    PaymentNotFoundError,
    PaymentCreationError,
    InvalidPaymentStatusTransition
)

router = APIRouter()


@router.post("/payments", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def api_create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    try:
        return create_payment(db, payload)
    except PaymentCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/payments", response_model=List[PaymentRead])
def api_list_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_payments(db, skip, limit)


@router.get("/payments/{payment_id}", response_model=PaymentRead)
def api_get_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        return get_payment(db, payment_id)
    except PaymentNotFoundError:
        raise HTTPException(status_code=404, detail="Payment not found")


@router.get("/payments/order/{order_id}", response_model=List[PaymentRead])
def api_get_payments_by_order(order_id: int, db: Session = Depends(get_db)):
    return list_payments_by_order(db, order_id)


@router.patch("/payments/{payment_id}/status", response_model=PaymentRead)
def api_update_payment_status(payment_id: int, payload: PaymentStatusUpdate, db: Session = Depends(get_db)):
    try:
        return update_payment_status(db, payment_id, payload)
    except PaymentNotFoundError:
        raise HTTPException(status_code=404, detail="Payment not found")
    except InvalidPaymentStatusTransition as e:
        raise HTTPException(status_code=400, detail=str(e))


# Webhook endpoint example
@router.post("/payments/webhook/{provider}")
async def provider_webhook(provider: str, request: Request, db: Session = Depends(get_db)):
    """
    Example webhook endpoint:
    - Accept provider result (JSON)
    - Validate signature / idempotency header (provider-specific)
    - Find payment by provider transaction id or custom reference (not shown here)
    - Update payment status using update_payment_status
    """
    payload = await request.json()

    # Example: provider sends {"payment_id": 123, "status": "completed"}
    # In a real integration, providers send provider_transaction_id and you map it to payment.id
    payment_id = payload.get("payment_id")
    status_str = payload.get("status")

    if not payment_id or not status_str:
        raise HTTPException(status_code=400, detail="Missing payment_id or status in webhook payload")

    try:
        status_enum = PaymentStatus(status_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Unknown status value")

    try:
        updated = update_payment_status(db, payment_id, PaymentStatusUpdate(status=status_enum))
    except PaymentNotFoundError:
        # idempotent handling: if we can't find a payment, log and return 200/400 depending on policy
        # return 404 could cause the provider to retry; decide per your policy
        raise HTTPException(status_code=404, detail="Payment not found")
    except InvalidPaymentStatusTransition as e:
        # For example, provider sends completed for an already completed payment -> we can return 200
        raise HTTPException(status_code=400, detail=str(e))

    # respond 200 to acknowledge the webhook
    return {"ok": True, "payment_id": updated.id, "status": updated.status}
