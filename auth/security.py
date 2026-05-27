from datetime import UTC, datetime, timedelta
from typing import Any
import jwt
from pwdlib import PasswordHash
from settings import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed: str,
) -> bool:
    return password_hash.verify(
        password,
        hashed,
    )


def create_access_token(
    user_id: int,
) -> str:
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "exp": datetime.now(UTC) + timedelta(hours=1),
    }

    secret_key: str = settings.SECRET_KEY

    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        payload,
        secret_key,
        algorithm="HS256",
    )
