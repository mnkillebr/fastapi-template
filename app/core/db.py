from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the asynchronous engine.
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create an async session factory.
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=settings.EXPIRE_ON_COMMIT)

async def init_db():
    async with engine.begin() as conn:
        # Create tables from all SQLModel models.
        await conn.run_sync(SQLModel.metadata.create_all)