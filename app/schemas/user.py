import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str  # raw password in, only ever hashed before hitting the DB


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    # Matches the User model but deliberately excludes hashed_password --
    # this is the shape returned to clients, never the ORM object directly.
    id: uuid.UUID
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"