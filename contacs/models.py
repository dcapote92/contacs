from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional


@dataclass
class Contact(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
