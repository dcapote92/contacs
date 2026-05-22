from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from .schemas import ContactCreate, ContactResponse, ContactUpdate
from .service import create_contact, list_contacts


router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
)

fake_db: list[ContactResponse] = []


# get all contacts
@router.get(
    "",
    response_model=list[ContactResponse],
)
async def list_contacts_route(
    db: Session = Depends(get_db),
):
    contacts = list_contacts(db=db)
    return contacts


# get contact by id
@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
)
async def get_contact(contact_id: int) -> ContactResponse:
    for contact in fake_db:
        if contact.id == contact_id:
            return contact

    raise HTTPException(
        status_code=404,
        detail="Contact not found",
    )


# create contact
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


# delete contact
@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_contact(contact_id: int):
    for index, contact in enumerate(fake_db):
        if contact.id == contact_id:
            fake_db.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Contact not found",
    )


# update contact
@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
)
async def update_contact(contact_id: int, data: ContactUpdate) -> ContactResponse:
    for index, contact in enumerate(fake_db):
        if contact.id == contact_id:
            updated_contact = contact.model_copy(update=data.model_dump(exclude_unset=True))
            fake_db[index] = updated_contact
            return updated_contact

    raise HTTPException(
        status_code=404,
        detail="Contact not found",
    )
