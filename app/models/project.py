from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from uuid import UUID

from .base import Base

if TYPE_CHECKING:
    from .task import Task
    from .goal import Goal
    from .users_projects_association import UserProjectAssociation

class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(
        default="No project description",
        server_default="No project description",
    )
    creator_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    goals: Mapped[list["Goal"]] = relationship(back_populates="project")
    tasks: Mapped[list["Task"]] = relationship(back_populates="project")

    executors: Mapped[list["UserProjectAssociation"]] = relationship(
        back_populates="user"
    )