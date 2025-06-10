import jwt
import bcrypt

from datetime import timedelta, datetime, timezone

from fastapi import Form, HTTPException, status
from sqlalchemy import insert

from models.user import User
from backend.session import async_session_maker
from backend.config import settings
from schemas.users import LoginUserSchema
from .base import BaseService

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
       to_encode,
       private_key,
       algorithm=algorithm,
    )
    return encoded

def decoded_jwt(
    token: str | bytes,
    key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token, 
        key, 
        algorithms=[algorithm],
    )
    return decoded

def create_jwt(
        token_type: str, 
        payload: dict,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(payload)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )

def create_access_token(user: LoginUserSchema) -> str:
    jwt_payload = {
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE, 
        payload=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )

def create_refresh_token(user:LoginUserSchema) -> str:
    jwt_payload = {
        "sub": user.email,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE, 
        payload=jwt_payload,
        expire_timedelta=timedelta(settings.auth_jwt.refresh_token_expire_days),
    )

class UserService(BaseService):
    model = User

    @classmethod
    def hash_password(cls, password: str) -> bytes:
        salt = bcrypt.gensalt()
        password_bytes: bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)

    @classmethod
    def validate_password(
        cls,
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
    
    @classmethod
    async def validation_authentificate_user(
        cls,
        email: str = Form(),
        password: str = Form(),
    ):
        is_user = await (cls.get_one_or_none(email=email))
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

        if is_user is None:
            raise unauthed_exc
        
        if cls.validate_password(
            password=password,
            hashed_password=is_user.hashed_password,
        ):
            return is_user
        
        raise unauthed_exc

    @classmethod
    async def create_user(cls, **user_data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**user_data)
            await session.execute(stmt)
            await session.commit()
