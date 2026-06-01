from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db


DBSession = Annotated[
    AsyncSession,
    Depends(get_db),
]
