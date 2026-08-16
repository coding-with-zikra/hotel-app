import uuid

from pydantic import BaseModel


class PaymentIntentCreate(BaseModel):
    booking_id: uuid.UUID


class PaymentIntentOut(BaseModel):
    client_secret: str
    payment_intent_id: str
    amount: int