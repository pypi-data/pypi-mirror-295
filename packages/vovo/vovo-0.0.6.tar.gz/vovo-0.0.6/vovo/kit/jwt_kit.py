from datetime import datetime, timedelta, UTC
from typing import Any

import jwt

DEFAULT_EXPIRATION = 60 * 60  # 60 minutes
ALGORITHM = "HS256"

DecodeError = jwt.DecodeError
ExpiredSignatureError = jwt.ExpiredSignatureError


def create_expiration_dt(seconds: int) -> datetime:
    return datetime.now(UTC) + timedelta(seconds=seconds)


def encode(
    *,
    data: dict[str, Any],
    secret: str,
    expires_at: datetime | None = None,
    expires_in: int | None = DEFAULT_EXPIRATION
) -> str:

    to_encode = data.copy()
    if not expires_at:
        expires_in = expires_in or DEFAULT_EXPIRATION
        expires_at = create_expiration_dt(seconds=expires_in)

    to_encode["exp"] = expires_at
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)


def decode_unsafe(*, token: str, secret: str) -> dict[str, Any]:
    return jwt.decode(token, secret, algorithms=[ALGORITHM])


def decode(
    *,
    token: str,
    secret: str,
) -> dict[str, Any]:
    res = decode_unsafe(token=token, secret=secret)

    if res.get("type", "") != type:
        raise Exception(
            "JWT of unexpected type, expected '%s' got '%s'", type, res.get("type", "")
        )

    return res
