"""
Stripe payment integration. Creates a PaymentIntent for a booking, and
handles the webhook Stripe calls back with once payment succeeds.

Requires STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET in the environment
(see app/core/config.py) -- never hardcoded.
"""
import stripe
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.booking import Booking

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(db: Session, booking_id, room_price_per_night: float, nights: int) -> dict:
    booking = db.get(Booking, booking_id)
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found.")

    # Stripe expects amounts in the smallest currency unit (paise/cents),
    # never a float -- floats would risk rounding errors on real money.
    amount_in_smallest_unit = int(round(room_price_per_night * nights * 100))

    intent = stripe.PaymentIntent.create(
        amount=amount_in_smallest_unit,
        currency="usd",
        metadata={"booking_id": str(booking_id)},
    )

    return {
        "client_secret": intent.client_secret,
        "payment_intent_id": intent.id,
        "amount": amount_in_smallest_unit,
    }


def confirm_payment_and_update_booking(db: Session, payment_intent) -> None:
    """
    Called from the webhook once Stripe confirms a payment succeeded.
    We trust payment_intent.metadata.booking_id (set by us when the
    intent was created) to find which booking to mark confirmed --
    never trust anything from the request body directly, only what
    Stripe's verified webhook payload contains.
    """
    booking_id = payment_intent.get("metadata", {}).get("booking_id")
    if not booking_id:
        return

    booking = db.get(Booking, booking_id)
    if booking is None:
        return

    booking.status = "confirmed"
    db.commit()
    