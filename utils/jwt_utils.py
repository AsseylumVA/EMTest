from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone


def create_jwt(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "iat": int(timezone.now().timestamp()),
        "exp": int(
            (timezone.now() + timedelta(minutes=settings.JWT_TTL_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
