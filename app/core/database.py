from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/fastapi_tutorial"

# Создаём асинхронный движок
engine = create_async_engine(url=DATABASE_URL, echo=True)

# Создаём асинхронный sessionmaker (современный стиль)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,         # движок, к которому привязываем сессии
    expire_on_commit=False  # объекты не “исчезают” после коммита
)

# Базовый класс для моделей
class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.

    Содержит общие поля и настройки для всех таблиц.
    """


async def get_db():
    """
    Генератор зависимостей для маршрутов FastAPI.
    Используем `async with` для безопасного закрытия сессии.
    """
    async with AsyncSessionLocal() as session:
        yield session


DBSession: type[AsyncSession] = Annotated[AsyncSession, Depends(get_db)]