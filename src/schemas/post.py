from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreatePostRequest(BaseModel):
    """Схема запроса для эндпоинта создания сущности 'Пост'."""

    goal_id: UUID
    title: str = Field(max_length=40)
    content: str


class PostResponse(BaseModel):
    """Схема ответа на эндпоинты сущности 'Пост'."""

    id: UUID
    goal_id: UUID
    title: str = Field(max_length=40)
    content: str
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
