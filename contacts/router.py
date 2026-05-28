from fastapi import APIRouter, status, HTTPException
from contacts.schemas import ContactCreate, ContactResponse, ContactUpdate
from contacts.service import create_contact, get_contacts, get_contact_by_id, update_contact, delete_contact
from contacts.models import ContactModel
from core.dependencies import DBSession, CurrentUser


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
    current_user: CurrentUser,
    db: DBSession,
):
    contact = create_contact(
        db=db,
        data=data,
        current_user=current_user,
    )
    return contact


# R
@router.get(
    "",
    response_model=list[ContactResponse],
)
async def list_contacts_route(
    current_user: CurrentUser,
    db: DBSession,
):
    contacts = get_contacts(
        db=db,
        curren_user=current_user,
    )
    return contacts


# R
@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
)
async def get_contact_by_id_route(
    contact_id: int,
    current_user: CurrentUser,
    db: DBSession,
) -> ContactModel | None:
    contact = get_contact_by_id(
        db=db,
        contact_id=contact_id,
        current_user=current_user,
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
    current_user: CurrentUser,
    db: DBSession,
) -> ContactModel:

    contact = update_contact(
        db=db,
        contact_id=contact_id,
        data=data,
        current_user=current_user,
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
    current_user: CurrentUser,
    db: DBSession,
):
    target = delete_contact(
        db=db,
        contact_id=contact_id,
        current_user=current_user,
    )

    if not target:
        raise HTTPException(
            status_code=404,
            detail="Contact not found",
        )
    return target
