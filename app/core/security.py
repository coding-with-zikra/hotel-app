"""
Auth primitives: password hashing + JWT create/verify.
Kept framework-agnostic (no FastAPI imports) so it can be unit tested
in isolation and reused by services.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def hash_password(plain_password: str) -> str:
    # bcrypt works on bytes and has a 72-byte input limit -- encode first.
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    'subject' is what the token identifies -- we use the user's id (as a string).
    'exp' (expiry) and 'sub' are standard JWT claims; jose/PyJWT check 'exp'
    automatically on decode and raise if the token has expired.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """
    Returns the subject (user id) if the token is valid and not expired,
    otherwise None. Callers (deps.get_current_user) turn None into a 401.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None