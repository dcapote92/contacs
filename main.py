from fastapi import FastAPI
from contacts.router import router as contacts_router
from auth.router import router as auth_router

app = FastAPI()

app.include_router(contacts_router)
app.include_router(auth_router)


@app.get("/")
async def home():
    return {"message": "Contact CRM!"}
