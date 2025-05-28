from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from uuid import UUID

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.users_projects_association import UserProjectAssociation

class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(
        default="No project description",
        server_default="No project description",
    )
    creator_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    goal_id: Mapped[UUID] = mapped_column(ForeignKey("goals.id"))
    tasks: Mapped[list["Task"]] = relationship(back_populates="project")

    executors: Mapped[list["UserProjectAssociation"]] = relationship(
        back_populates="user"
    )