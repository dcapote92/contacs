from fastapi import FastAPI
from database import Base, engine
from contacts.router import router as contacts_router

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(contacts_router)


@app.get("/")
async def home():
    return {"message": "Contact CRM!"}
