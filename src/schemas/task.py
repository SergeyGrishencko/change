from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateTaskRequest(BaseModel):
    """Схема запроса для эндпоинта создания сущности 'Задача'."""

    goal_id: UUID
    title: str = Field(max_length=40)
    description: str


class TaskResponse(BaseModel):
    """Схема ответа на эндпоинты сущности 'Задача'."""

    id: UUID
    goal_id: UUID
    title: str = Field(max_length=40)
    description: str
    is_completed: bool
    user_id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    finished_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
