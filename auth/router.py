from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.schemas import TokenResponse, UserLogin, UserRegister
from auth.service import login_user, register_user
from database import get_db
from typing import Any


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(
    data: UserRegister,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    try:
        user = register_user(
            db=db,
            data=data,
        )
        return {
            "id": user.id,
            "email": user.email,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: UserLogin,
    db: Session = Depends(get_db),
):
    token = login_user(
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
