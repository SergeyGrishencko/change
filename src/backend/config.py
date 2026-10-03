from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"    
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    DB_PASS: str = "postgres"
    DB_USER: str = "postgres"

    @model_validator(mode='before')
    def get_database_url(cls, v):
        v['DATABASE_URL'] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        return v
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings() 