from fastapi import HTTPException, status

from services.users import (
    UserService
)
from schemas.users import RegisterUserSchema

async def register_user(user_data: RegisterUserSchema):
    is_user = await UserService.get_one_or_none(email=user_data.email)
    if is_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This Email has already been registered."
        )
    hashed_password = UserService.hash_password(password=user_data.password)
    await UserService.create_user(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hashed_password,
        description=user_data.description,
    )
    return is_user