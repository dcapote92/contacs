from fastapi import HTTPException, status
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from contacts.models import ContactModel
from contacts.schemas import ContactCreate, ContactUpdate
from auth.models import UserModel
from core.types import CurrentUser
from typing import Any


async def create_contact(
    db: AsyncSession,
    data: ContactCreate,
    current_user: CurrentUser,
) -> ContactModel:

    contact = ContactModel(
        **data.model_dump(),
        user_id=current_user.id,
    )

    db.add(contact)
    await db.commit()
    await db.refresh(contact)

    return contact


async def get_contacts(
    db: AsyncSession,
    current_user: UserModel,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
) -> dict[str, Any]:

    statement = select(ContactModel).where(
        ContactModel.user_id == current_user.id,
    )

    if search:
        statement = statement.where(
            or_(
                ContactModel.name.ilike(f"%{search}%"),
                ContactModel.email.ilike(f"%{search}%"),
                ContactModel.phone.ilike(f"%{search}%"),
            )
        )

    total = await db.scalar(
        select(func.count()).select_from(
            statement.subquery(),
        ),
    )

    statement = statement.offset(skip).limit(limit)

    result = await db.execute(statement)
    contacts: list[ContactModel] = list(result.scalars().all())

    return {
        "items": contacts,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


async def get_contact_by_id(
    db: AsyncSession,
    contact_id: int,
    current_user: CurrentUser,
):

    statement = select(ContactModel).where(
        ContactModel.id == contact_id,
        ContactModel.user_id == current_user.id,
    )
    contact = await db.scalars(statement)

    return contact.first()


async def update_contact(
    db: AsyncSession,
    contact_id: int,
    data: ContactUpdate,
    current_user: CurrentUser,
):
    contact = await get_contact_by_id(
        db=db,
        contact_id=contact_id,
        current_user=current_user,
    )

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    if data.name is not None:
        contact.name = data.name
    if data.email is not None:
        contact.email = data.email
    if data.phone is not None:
        contact.phone = data.phone

    await db.commit()
    await db.refresh(contact)
    return contact


async def delete_contact(
    db: AsyncSession,
    contact_id: int,
    current_user: CurrentUser,
):
    contact = await get_contact_by_id(
        db=db,
        contact_id=contact_id,
        current_user=current_user,
    )

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    await db.delete(contact)
    await db.commit()
    return {"message": "Contact deleted successfully"}
