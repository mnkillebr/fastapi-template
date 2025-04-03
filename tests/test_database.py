import pytest
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from app.dependencies import get_session
from app.core.db import async_session


@pytest.fixture
async def mock_engine(mocker):
    # Mock the engine
    mock_engine = mocker.AsyncMock(spec=AsyncEngine)

    # Create a mock connection
    mock_conn = mocker.AsyncMock()
    mock_conn.run_sync = mocker.AsyncMock()

    # Set up the context manager properly
    mock_context = mocker.AsyncMock()
    mock_context.__aenter__.return_value = mock_conn
    mock_engine.begin.return_value = mock_context

    return mock_engine


@pytest.fixture
async def mock_session(mocker):
    # Create a mock session
    mock_session = mocker.AsyncMock(spec=AsyncSession)

    # Mock the session context manager
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None

    # Mock the session maker
    mock_session_maker = mocker.patch("app.core.db.async_session")
    mock_session_maker.return_value = mock_session

    return mock_session


@pytest.mark.asyncio
async def test_get_async_session(mock_session):
    # Test the session generator
    session_generator = get_session()
    session = await session_generator.__anext__()

    # Verify we got the mock session
    assert session == mock_session

    # Verify the session was created with the expected context
    mock_session.__aenter__.assert_called_once()



def test_engine_creation(mocker):
    # Mock settings
    mock_settings = mocker.patch("app.core.config")
    mock_settings.DATABASE_URL = "sqlite+aiosqlite:///./test.db"
    mock_settings.EXPIRE_ON_COMMIT = False

    # Import engine to trigger creation with mocked settings
    from app.core.db import engine, async_session

    # Verify engine is created
    assert isinstance(engine, AsyncEngine)

    # Verify session maker is configured
    assert async_session.kw["expire_on_commit"] is False


@pytest.mark.asyncio
async def test_session_maker_configuration():
    # Create a test session
    async with async_session() as session:
        assert isinstance(session, AsyncSession)