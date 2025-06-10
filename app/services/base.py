from sqlalchemy import select

from backend.session import async_session_maker

class BaseService:
    model = None

    @classmethod
    async def get_one_or_none(cls, **filter_data):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_data)
            result = await session.execute(query)
            return result.scalar_one_or_none()