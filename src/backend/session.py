from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.backend.config import settings

engine = create_async_engine(url=settings.DATABASE_URL) # type: ignore
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def database_session() -> AsyncGenerator[AsyncSession, None]:
    """Отдает сессию подключения к базе данных."""
    async with async_session_maker() as session:
        yield session