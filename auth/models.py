from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )
    password_hash: Mapped[str]

    contacts = relationship(
        "ContactModel",
        back_populates="user",
    )
