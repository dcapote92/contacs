from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class ContactModel(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str | None]
