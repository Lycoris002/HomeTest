from typing import AsyncGenerator
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB
from sqlalchemy import create_engine as sync_create_engine

Base = declarative_base()


def get_database_url() -> str:
    """
    Construct the database URL for SQLAlchemy.
    """
    return f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"


engine = create_async_engine(get_database_url())
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new database session.
    """
    async with session_factory() as session:
        yield session


def init_test_database() -> None:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    test_db_path = os.path.join(project_root, "test.db")
    test_url = f"sqlite:///{test_db_path}"
    test_engine = sync_create_engine(test_url, echo=False)

    with test_engine.begin():
        Base.metadata.create_all(test_engine)
    print("Test Database Initialized Successfully")
