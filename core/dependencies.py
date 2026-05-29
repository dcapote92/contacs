from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from auth.models import UserModel
from auth.dependencies import get_current_user

DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[UserModel, Depends(get_current_user)]
