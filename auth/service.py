from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models import UserModel
from auth.schemas import UserRegister
from core.security import (
    hash_password,
    create_access_token,
    verify_password,
)


async def register_user(
    db: AsyncSession,
    data: UserRegister,
) -> UserModel:
    existing_user = await db.scalar(
        select(UserModel).where(UserModel.email == data.email),
    )

    if existing_user:
        raise ValueError("Email already registered")

    user = UserModel(
        email=data.email,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def login_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> str | None:
    user: UserModel | None = await db.scalar(
        select(UserModel).where(UserModel.email == email),
    )

    if user is None:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return create_access_token(
        user.id,
    )
