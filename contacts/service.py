from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import ContactModel
from .schemas import ContactCreate


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
