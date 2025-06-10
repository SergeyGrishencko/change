from pydantic import BaseModel, EmailStr, ConfigDict

class UserTokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"

class RegisterUserSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str
    description: str | None = None

class LoginUserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    password: str