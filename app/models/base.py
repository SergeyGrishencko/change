from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import date, datetime, timezone
from uuid import uuid4, UUID
from sqlalchemy import Date

class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    create_date: Mapped[date] = mapped_column(Date, default=datetime.now(timezone.utc))
    finished_date: Mapped[date] = mapped_column(Date, default=datetime.now(timezone.utc))