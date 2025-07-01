from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import database_config
from sqlalchemy.orm import declarative_base

DATABASE_URL = database_config.database_url

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=database_config.echo,
    pool_size=database_config.pool_size,
    max_overflow=database_config.max_overflow,
)

# Base for your models


# Async session factory
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
Base = declarative_base()
# Dependency for FastAPI routes
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
