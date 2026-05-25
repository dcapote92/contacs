from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import ContactModel
from .schemas import ContactCreate, ContactUpdate


def create_contact(
    db: Session,
    data: ContactCreate,
) -> ContactModel:

    contact = ContactModel(
        name=data.name,
        email=data.email,
        phone=data.phone,
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def list_contacts(
    db: Session,
) -> list[ContactModel]:

    statement = select(ContactModel)
    contacts = list(db.scalars(statement).all())

    return contacts


def get_contact_by_id(
    db: Session,
    contact_id: int,
):

    statement = select(ContactModel).where(ContactModel.id == contact_id)
    contact = db.scalars(statement).first()

    return contact


def update_contact(
    db: Session,
    contact_id: int,
    data: ContactUpdate,
):
    contact = get_contact_by_id(db=db, contact_id=contact_id)

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
):
    contact = get_contact_by_id(db=db, contact_id=contact_id)

    if not contact:
        return None
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted successfully"}
