from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text

from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    #Add relationships