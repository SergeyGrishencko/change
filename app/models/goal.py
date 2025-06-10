from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text
from uuid import UUID

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .task import Task
    from .project import Project

class Goal(Base):
    __tablename__ = "goals"

    name: Mapped[str] = mapped_column(Text)

    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[UUID | None] = mapped_column(ForeignKey("projects.id"))

    user: Mapped["User"] = relationship(back_populates="goals")
    project: Mapped["Project"] = relationship(back_populates="goals")
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")