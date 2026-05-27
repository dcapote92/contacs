from sqlalchemy import select
from sqlalchemy.orm import Session
from auth.models import UserModel
from auth.schemas import UserRegister
from auth.security import hash_password, create_access_token, verify_password


def register_user(
    db: Session,
    data: UserRegister,
) -> UserModel:
    existing_user = db.scalar(select(UserModel).where(UserModel.email == data.email))

    if existing_user:
        raise ValueError("Email already registered")

    user = UserModel(
        email=data.email,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(
    db: Session,
    email: str,
    password: str,
) -> str | None:
    user = db.scalar(select(UserModel).where(UserModel.email == email))

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return create_access_token(
        user.id,
    )
