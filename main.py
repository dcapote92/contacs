from fastapi import FastAPI, status
from schemas.contacts import ContactCreate, ContactResponse

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
