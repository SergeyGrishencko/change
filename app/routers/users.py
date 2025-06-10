from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from schemas.users import RegisterUserSchema, LoginUserSchema, UserTokenInfo
from cruds.users import register_user
from services.users import UserService, create_access_token, create_refresh_token

http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login",
)

router = APIRouter(
    prefix="/user",
    tags=["Users"],
    # dependencies=[Depends(oauth2_scheme)]
)

@router.post("/register")
async def register(user_data: RegisterUserSchema):
    await register_user(user_data=user_data)

@router.post("/login")
async def login(
    user: LoginUserSchema = Depends(UserService.validation_authentificate_user)
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return UserTokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )