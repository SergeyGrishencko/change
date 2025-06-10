from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import Text, LargeBinary

from .base import Base

if TYPE_CHECKING:
    from .task import Task
    from .goal import Goal
    from .users_projects_association import UserProjectAssociation

class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str | None] = mapped_column(
        default="No first name",
        server_default="No first name",
    )
    last_name: Mapped[str | None] = mapped_column(
        default="No last name",
        server_default="No last name",
    )
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    description: Mapped[str | None] = mapped_column(
        Text,
        default="No user description",
        server_default="No user description",
    )

    tasks: Mapped[list["Task"]] = relationship(back_populates="user")
    goals: Mapped[list["Goal"]] = relationship(back_populates="user")
    projects: Mapped[list["UserProjectAssociation"]] = relationship(
        back_populates="project"
    )