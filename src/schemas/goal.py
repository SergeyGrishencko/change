from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.enums.goal import GoalStatusEnum


class CreateGoalRequest(BaseModel):
    """Схема запроса для эндпоинта создания сущности 'Цель'."""

    title: str = Field(max_length=40)
    description: str | None = None


class GoalResponse(BaseModel):
    """Схема ответа на эндпоинты сущности 'Цель'."""

    id: UUID
    title: str = Field(max_length=40)
    status: GoalStatusEnum
    user_id: UUID
    created_at: datetime
    description: str | None = None
    updated_at: datetime | None = None
    finished_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
