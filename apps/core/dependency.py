from typing import Annotated, AsyncIterator

from core.settings import config
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


async_engine = create_async_engine(config.async_dsn)  # type: ignore


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSession(async_engine) as session:
        yield session


AsyncSessionDepency = Annotated[
    AsyncSession, Depends(get_async_session, use_cache=True)
]
