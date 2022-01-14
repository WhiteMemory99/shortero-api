from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_async_engine(settings.get_database_uri(), future=True)
SessionFactory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True)


async def get_session() -> Generator:
    async with SessionFactory() as session:
        yield session
