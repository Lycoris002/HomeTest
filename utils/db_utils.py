from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from settings import (
    DB_TYPE,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
)

Base = declarative_base()


def get_database_url() -> str:
    if DB_TYPE == "postgres":
        return (
            f"postgresql+psycopg://"
            f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
            f"@localhost:5432/{POSTGRES_DB}"
        )

    if DB_TYPE == "sqlite":
        return "sqlite+aiosqlite:///./test.db"

    raise ValueError("Unsupported DB_TYPE")


engine = create_async_engine(
    get_database_url(),
    echo=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
