from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models  # <- этот импорт важен! Модели регистрируются здесь
from app.api.users_router import router as user_router
from app.api.dev_router import router as dev_router
from app.core.database import engine, Base
from app.web_router import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём или обновляем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(
    lifespan=lifespan
)

app.include_router(user_router)
app.include_router(web_router)
app.include_router(dev_router)
