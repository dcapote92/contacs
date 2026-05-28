from sqlalchemy.orm import Session
from sqlalchemy import select

from contacts.models import ContactModel
from contacts.schemas import ContactCreate, ContactUpdate
from auth.models import UserModel
from core.dependencies import CurrentUser


def create_contact(
    db: Session,
    data: ContactCreate,
    current_user: CurrentUser,
) -> ContactModel:

    contact = ContactModel(
        **data.model_dump(),
        user_id=current_user.id,
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def get_contacts(
    db: Session,
    curren_user: UserModel,
) -> list[ContactModel]:

    statement = select(ContactModel).where(
        ContactModel.user_id == curren_user.id,
    )
    contacts = list(db.scalars(statement).all())

    return contacts


def get_contact_by_id(
    db: Session,
    contact_id: int,
    current_user: CurrentUser,
):

    statement = select(ContactModel).where(
        ContactModel.id == contact_id,
        ContactModel.user_id == current_user.id,
    )
    contact = db.scalars(statement).first()

    return contact


def update_contact(
    db: Session,
    contact_id: int,
    data: ContactUpdate,
    current_user: CurrentUser,
):
    contact = get_contact_by_id(
        db=db,
        contact_id=contact_id,
        current_user=current_user,
    )

    if not contact:
        return None

    if data.name is not None:
        contact.name = data.name
    if data.email is not None:
        contact.email = data.email
    if data.phone is not None:
        contact.phone = data.phone

    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(
    db: Session,
    contact_id: int,
    current_user: CurrentUser,
):
    contact = get_contact_by_id(
        db=db,
        contact_id=contact_id,
        current_user=current_user,
    )

    if not contact:
        return None
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted successfully"}
