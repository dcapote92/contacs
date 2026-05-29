from fastapi import APIRouter, status, HTTPException
from contacts.schemas import ContactCreate, ContactResponse, ContactUpdate, ContactListResponse
from contacts.service import create_contact, get_contacts, get_contact_by_id, update_contact, delete_contact
from contacts.models import ContactModel
from core.dependencies import DBSession, CurrentUser


router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
)


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


@router.get(
    "",
    response_model=ContactListResponse,
)
async def list_contacts_route(
    current_user: CurrentUser,
    db: DBSession,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
):

    contacts = await get_contacts(
        db=db,
        current_user=current_user,
        skip=skip,
        limit=limit,
        search=search,
    )
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
)
async def get_contact_by_id_route(
    contact_id: int,
    current_user: CurrentUser,
    db: DBSession,
) -> ContactModel | None:
    contact: ContactModel | None = await get_contact_by_id(
        db=db,
        contact_id=contact_id,
        current_user=current_user,
    )
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return contact


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

    contact: ContactModel = await update_contact(
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


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_contact_route(
    contact_id: int,
    current_user: CurrentUser,
    db: DBSession,
):
    target = await delete_contact(
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
