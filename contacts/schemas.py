from pydantic import BaseModel, EmailStr
from typing import Optional


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class ContactResponse(ContactCreate):
    id: int


class ContactListResponse(BaseModel):
    items: list[ContactResponse]
    total: int
    skip: int
    limit: int


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
