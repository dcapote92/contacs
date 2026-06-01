from typing import Annotated
from fastapi import Depends
from auth.dependencies import get_current_user, require_role
from auth.models import UserModel
from auth.enums import UserRole

CurrentUser = Annotated[UserModel, Depends(get_current_user)]

CurrentUserRole = Annotated[
    UserModel,
    Depends(
        require_role(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
]
