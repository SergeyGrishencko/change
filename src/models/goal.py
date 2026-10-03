from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.enums.goal import GoalStatusEnum
from src.models.base import Base

if TYPE_CHECKING:
    from .post import Post
    from .task import Task
    from .user import User

class Goal(Base):
    __tablename__ = 'goals'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    title: Mapped[str] = mapped_column(String(length=40), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[GoalStatusEnum] = mapped_column(Enum(GoalStatusEnum), default=GoalStatusEnum.active)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(UTC))
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship(back_populates="goals")
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="goal", cascade="all, delete-orphan"
    )
    posts: Mapped[list["Post"]] = relationship(back_populates="goal")