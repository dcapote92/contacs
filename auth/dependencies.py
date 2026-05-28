from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from auth.models import UserModel
from core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserModel:

    payload = decode_token(token)

    user_id = int(payload["sub"])

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.scalar(select(UserModel).where(UserModel.id == user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
