from fastapi import APIRouter, HTTPException, status
from auth.schemas import TokenResponse, UserLogin, UserRegister
from auth.service import login_user, register_user, update_user_role
from typing import Any
from core.dependencies import DBSession
from core.types import CurrentUser
from auth.enums import UserRole


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(
    data: UserRegister,
    db: DBSession,
) -> dict[str, Any]:
    try:
        user = await register_user(
            db=db,
            data=data,
        )
        return {
            "id": user.id,
            "email": user.email,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: UserLogin,
    db: DBSession,
):
    token = await login_user(
        db=db,
        email=data.email,
        password=data.password,
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    return TokenResponse(
        access_token=token,
    )


@router.get("/me")
async def me(current_user: CurrentUser) -> dict[str, Any]:
    return {
        "id": current_user.id,
        "email": current_user.email,
    }


@router.patch("/users/{user_id}/role")
async def update_role(
    user_id: int,
    role: UserRole,
    db: DBSession,
):
    return await update_user_role(
        db=db,
        user_id=user_id,
        role=role,
    )
