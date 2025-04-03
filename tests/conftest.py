import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.main import app
from app.dependencies import get_session
from app.core.config import settings

@pytest_asyncio.fixture(scope="function")
async def engine():
    """Create a fresh test database engine for each test function."""
    engine = create_async_engine(settings.TEST_DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(engine):
    """Create a fresh database session for each test."""
    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=settings.EXPIRE_ON_COMMIT
    )

    async with async_session_maker() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture(scope="function")
async def test_client(db_session):
    """Fixture to create a test client that uses the test database session."""

    # General database override (raw session access)
    async def override_get_async_session():
        try:
            yield db_session
        finally:
            await db_session.close()

    # Set up test database overrides
    app.dependency_overrides[get_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as client:
        yield client