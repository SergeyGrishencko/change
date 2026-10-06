from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.security import hashed_password
from src.models.user import User
from src.schemas.user import RegisterUserRequest, UserResponse


class AuthService:

    @classmethod
    async def add_user(cls, user_data: RegisterUserRequest, session: AsyncSession) -> UserResponse:
        """Добавляет пользователя в БД, в таблицу User."""
        user_by_email = select(User).where(User.email == user_data.email)
        execute_transaction = await session.execute(user_by_email)
        existing_user = execute_transaction.scalar_one_or_none()

        if not existing_user:
            raise HTTPException(status_code=409)

        hash_password = hashed_password(password=user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password,
        )

        session.add(user)
        await session.commit()

        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at,
        )