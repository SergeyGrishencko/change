from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from .goal import Goal
    from .user import User

class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    title: Mapped[str] = mapped_column(String(length=40), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    goal_id: Mapped[UUID] = mapped_column(ForeignKey("goals.id"), nullable=False)

    owner: Mapped["User"] = relationship(back_populates="posts")
    goal: Mapped["Goal"] = relationship(back_populates="posts")