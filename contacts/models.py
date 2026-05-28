from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from datetime import datetime, UTC


class ContactModel(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship(
        "UserModel",
        back_populates="contacts",
    )
