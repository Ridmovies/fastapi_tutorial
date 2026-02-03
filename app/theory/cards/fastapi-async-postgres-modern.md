# FastAPI + Async PostgreSQL (SQLAlchemy 2.0, современный стиль)

## 1. Установка зависимостей

pip install fastapi sqlalchemy asyncpg

- fastapi — FastAPI с Pydantic и Uvicorn
- sqlalchemy — асинхронный SQLAlchemy
- asyncpg — драйвер PostgreSQL для async

---

## 2. Создание асинхронного движка и сессии


DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"

# Создаём асинхронный движок
engine = create_async_engine(
    DATABASE_URL,        # URL базы данных
    echo=True            # Логировать SQL-запросы в консоль
)

# Создаём асинхронный sessionmaker (современный стиль)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,         # движок, к которому привязываем сессии
    class_=AsyncSession, # используем асинхронную сессию
    expire_on_commit=False  # объекты не “исчезают” после коммита
)

# Базовый класс для моделей

    class Base(DeclarativeBase):
        """
        Базовый класс для всех моделей SQLAlchemy.
    
        Содержит общие поля и настройки для всех таблиц.
        """

---

## 3. Зависимость для FastAPI

from fastapi import Depends

async def get_db():
    """
    Генератор зависимостей для маршрутов FastAPI.
    Используем `async with` для безопасного закрытия сессии.
    """
    async with AsyncSessionLocal() as session:
        yield session

---

## 4. Пример модели в современном стиле

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)           # первичный ключ
    username: Mapped[str] = mapped_column(String, unique=True) # уникальная строка
    email: Mapped[str] = mapped_column(String, index=True)     # индексированная строка

---

## 5. Примеры асинхронного CRUD

from sqlalchemy.future import select

# Создание пользователя
async def create_user(db: AsyncSession, username: str, email: str):
    user = User(username=username, email=email)  # создаём объект модели
    db.add(user)                                 # добавляем в сессию
    await db.commit()                            # сохраняем в базе (await!)
    await db.refresh(user)                       # обновляем объект из БД
    return user

# Получение пользователя по ID
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).where(User.id == user_id)  # строим SELECT-запрос
    )
    return result.scalar_one_or_none()           # возвращаем один объект или None

---

💡 **Пояснения к каждой строчке:**

1. `create_async_engine(DATABASE_URL, echo=True)`  
   Создаёт асинхронный движок для работы с PostgreSQL.

2. `async_sessionmaker(...)`  
   Современный способ создавать сессии: безопасно и async-совместимо.

3. `expire_on_commit=False`  
   После коммита объекты остаются доступными без повторного запроса.

4. `async with AsyncSessionLocal() as session`  
   Гарантирует, что сессия закроется после использования.

5. `Mapped[...] = mapped_column(...)`  
   Типизированная колонка, современный стиль SQLAlchemy 2.0.

6. `await db.commit()` и `await db.refresh(user)`  
   Коммит сохраняет изменения в базе, refresh подтягивает актуальные данные.

7. `await db.execute(select(User).where(...))`  
   Асинхронный SELECT-запрос.

---

💡 **Советы по использованию:**

- Использовать **async_sessionmaker** вместо старого `sessionmaker` для асинхронного кода.
- Всегда использовать `async with` или генератор зависимостей в FastAPI.
- Никогда не смешивать синхронные и асинхронные сессии в одном приложении.
- Для миграций используйте Alembic с асинхронным движком (`async_engine`).

