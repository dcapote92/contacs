from pydantic import BaseModel, EmailStr
from typing import Optional


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class ContactResponse(ContactCreate):
    id: int
