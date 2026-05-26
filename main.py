from fastapi import FastAPI
from contacts.router import router as contacts_router

app = FastAPI()

app.include_router(contacts_router)


@app.get("/")
async def home():
    return {"message": "Contact CRM!"}
