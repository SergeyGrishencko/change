from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterUserRequest(BaseModel):
    """Схема запроса для эндпоинта регистрации пользователя."""

    email: EmailStr
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    """Схема ответа на эндпоинты сущности 'Пользователь'."""

    id: UUID
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
