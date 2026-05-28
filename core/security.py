from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import UTC, datetime, timedelta
from typing import Any
import jwt
from pwdlib import PasswordHash
from core.settings import settings
from database import get_db
from auth.models import UserModel

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    try:
        payload = jwt.decode(  # pyright: ignore[reportUnknownMemberType]
            token,
            settings.SECRET_KEY,
            algorithms="HS256",
        )

        user_id = int(payload["sub"])

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.get(
        UserModel,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
