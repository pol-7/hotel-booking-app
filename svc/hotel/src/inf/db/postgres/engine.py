from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from . import config


class Base(DeclarativeBase):
    pass


engine = create_async_engine(config.ALCHEMY_DB_URI, echo=False)
smaker = async_sessionmaker(
    engine, autocommit=False, autoflush=False, expire_on_commit=False
)


@asynccontextmanager
async def get_db():
    async with smaker() as session:
        yield session
