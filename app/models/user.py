from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import Text

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.goal import Goal
    from app.models.users_projects_association import UserProjectAssociation

class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
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