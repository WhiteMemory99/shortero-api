import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.dependencies.database import get_session
from app.main import app
from app.models import Base

test_engine = create_async_engine(settings.get_database_uri() + "_test", future=True)
TestSessionFactory = sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession, future=True
)


async def get_test_session() -> Generator:
    """Overridden dependency to get the test session to endpoints"""
    async with TestSessionFactory() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db() -> Generator:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def client() -> Generator:
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
