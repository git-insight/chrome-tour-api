"""Database configuration module for async SQLAlchemy sessions with PostgreSQL."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Define the database connection URL for PostgreSQL with asyncpg driver
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5433/chrome_users_db"

# Create an asynchronous SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory bound to the async engine
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """
    Provides a database session to endpoints using dependency injection.

    This function is designed to be used with FastAPI's Depends system.
    It yields a session and ensures proper cleanup after the request is handled.
    """
    async with async_session() as session:
        yield session
