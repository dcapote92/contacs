from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from .schemas import ContactCreate, ContactResponse, ContactUpdate
from .service import create_contact, get_contacts, get_contact_by_id, update_contact, delete_contact
from .models import ContactModel
from auth.dependencies import get_current_user
from auth.models import UserModel


router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
)


"""
CRUD stands for Create, Read, Update, Delete.
These are the four basic operations that can be performed on data in a database or an application.
C - Create
R - Read
U - Update
D - Delete
"""


# C
@router.post(
    "",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact_route(
    data: ContactCreate,
    db: Session = Depends(get_db),
):
    contact = create_contact(
        db=db,
        data=data,
    )
    return contact


# R
@router.get(
    "",
    response_model=list[ContactResponse],
)
async def list_contacts_route(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    contacts = get_contacts(db=db, curren_user=current_user)
    return contacts


# R
@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
)
async def get_contact_by_id_route(
    contact_id: int,
    db: Session = Depends(get_db),
) -> ContactModel | None:
    contact = get_contact_by_id(
        db=db,
        contact_id=contact_id,
    )
    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found",
        )

    return contact


# U
@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
)
async def update_contact_route(
    contact_id: int,
    data: ContactUpdate,
    db: Session = Depends(get_db),
) -> ContactModel:

    contact = update_contact(
        db=db,
        contact_id=contact_id,
        data=data,
    )
    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found",
        )
    return contact


# D
@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_contact_route(
    contact_id: int,
    db: Session = Depends(get_db),
):
    target = delete_contact(db=db, contact_id=contact_id)

    if not target:
        raise HTTPException(
            status_code=404,
            detail="Contact not found",
        )
    return target
