# app/user_database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Define the database URL for user management
SQLALCHEMY_USERDB_URL = "postgresql+asyncpg://postgres:password@localhost:5432/chrome_users_db"

# Create the SQLAlchemy engine for async use
userdb_engine = create_async_engine(SQLALCHEMY_USERDB_URL, echo=True)

# Create session maker for async SQLAlchemy sessions
UserSessionLocal = sessionmaker(
    bind=userdb_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for declarative models (User-related tables)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
