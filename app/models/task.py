from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey
from uuid import UUID
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .project import Project
    from .goal import Goal

class Task(Base):
    __tablename__ = "tasks"

    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(
        Text,
        default="No description",
        server_default="No description",
    )
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[UUID | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    goal_id: Mapped[UUID | None] = mapped_column(ForeignKey("goals.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="tasks")
    goal: Mapped["Goal"] = relationship(back_populates="tasks")
    project: Mapped["Project"] = relationship(back_populates="tasks")