from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint, ForeignKey
from typing import TYPE_CHECKING
from uuid import UUID

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project

class UserProjectAssociation(Base):
    __tablename__ = "user_project_association"
    __table_args__ = (
        UniqueConstraint(
            "user_id", 
            "project_id", 
            name="idx_unique_user_project"
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"))

    user: Mapped["User"] = relationship(back_populates="executors")
    project: Mapped["Project"] = relationship(back_populates="projects")