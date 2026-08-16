import stripe
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.booking import Booking
from app.models.room import Room
from app.schemas.payment import PaymentIntentCreate, PaymentIntentOut
from app.services import payment_service

router = APIRouter(tags=["payments"])


@router.post("/payments/create-intent", response_model=PaymentIntentOut)
def create_intent(
    payload: PaymentIntentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = db.get(Booking, payload.booking_id)
    if booking is None or booking.user_id != current_user.id:
        # Same error whether the booking doesn't exist or belongs to
        # someone else -- don't reveal which via the error message.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found.")

    room = db.get(Room, booking.room_id)
    nights = (booking.check_out - booking.check_in).days

    return payment_service.create_payment_intent(
        db, booking.id, float(room.price_per_night), nights
    )


@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        # construct_event verifies the payload was actually signed by
        # Stripe using our webhook secret -- without this check, anyone
        # could POST a fake "payment succeeded" event to this endpoint
        # and confirm bookings without ever paying.
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook signature.")

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        payment_service.confirm_payment_and_update_booking(db, payment_intent)

    return {"status": "received"}