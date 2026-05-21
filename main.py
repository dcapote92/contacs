from fastapi import FastAPI
from contacs.models import Contact

app = FastAPI()

fake_db: list[Contact] = []


@app.get("/")
async def home():
    return {"message": "Contact CRM!"}


@app.get("/contacts")
async def list_contacts():
    return fake_db


@app.post("/contacts")
async def create_contact(contact: Contact) -> dict:
    fake_db.append(contact)

    return {
        "message": "Contact created successfully!",
        "data": contact,
    }
