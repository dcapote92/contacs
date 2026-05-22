from fastapi import FastAPI, status, HTTPException
from schemas.contacts import ContactCreate, ContactResponse, ContactUpdate

app = FastAPI()

fake_db: list[ContactResponse] = []


@app.get("/")
async def home():
    return {"message": "Contact CRM!"}


@app.get(
    "/contacts",
    response_model=list[ContactResponse],
)
async def list_contacts():
    return fake_db


@app.get(
    "/contacts/{contact_id}",
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


@app.post(
    "/contacts",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(contact: ContactCreate) -> ContactResponse:
    new_contact = ContactResponse(
        id=len(fake_db) + 1,
        name=contact.name,
        email=contact.email,
        phone=contact.phone,
    )

    fake_db.append(new_contact)

    return new_contact


@app.delete(
    "/contacts/{contact_id}",
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


@app.put(
    "/contacts/{contact_id}",
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
