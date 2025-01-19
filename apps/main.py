from contextlib import asynccontextmanager

from core.dependency import async_engine
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from models.base import Base

from api.application import app_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await async_engine.dispose()
    yield


app = FastAPI(lifespan=lifespan)
add_pagination(app)


app.include_router(app_router)
