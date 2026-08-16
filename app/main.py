from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import auth, rooms, bookings, payments, menu, food_orders

app = FastAPI(title=settings.PROJECT_NAME)

# Wide open for local dev; tighten to the real frontend origin(s) in prod.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(rooms.router, prefix=settings.API_V1_PREFIX)
app.include_router(bookings.router, prefix=settings.API_V1_PREFIX)
app.include_router(payments.router, prefix=settings.API_V1_PREFIX)
app.include_router(menu.router, prefix=settings.API_V1_PREFIX)
app.include_router(food_orders.router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
def health_check():
    return {"status": "ok"}