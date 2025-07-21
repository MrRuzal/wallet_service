from typing import Final
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

DATABASE_URL: Final[str] = settings.database_url

engine = create_async_engine(
    DATABASE_URL, echo=settings.SQLALCHEMY_ECHO, future=True
)

async_session: sessionmaker[AsyncSession] = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
