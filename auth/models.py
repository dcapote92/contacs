from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from enum import Enum


class UserRole(str, Enum):
    ADMIN = ("admin",)
    MANAGER = ("manager",)
    AGENT = ("agent",)
    VIEWER = ("viewer",)


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )
    password_hash: Mapped[str]

    role: Mapped[UserRole] = mapped_column(
        default=UserRole.AGENT,
    )

    contacts = relationship(
        "ContactModel",
        back_populates="user",
    )
