from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.session import database_session
from src.schemas.user import RegisterUserRequest, UserResponse
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Регистрация и аутентификация пользователей"])

@router.post("/register")
async def register_user(
    request: RegisterUserRequest, 
    session: AsyncSession = Depends(database_session),
) -> UserResponse | None:
    """Эндпоинт регистрации пользователя в системе."""

    try:
        result = await AuthService.add_user(user_data=request, session=session)
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Email already exist')
    
    return result