```
# FastAPI: @asynccontextmanager и lifespan

FastAPI >= 0.95 поддерживает **жизненный цикл приложения** через `lifespan`.  
Это **асинхронная альтернатива** старым `startup` и `shutdown` событиям.

---

## 1. Основная форма

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("🚀 Starting application...")
    
    yield  # здесь приложение готово к обработке запросов

    # Shutdown logic
    print("🛑 Shutting down application...")
```

- `yield` разделяет **startup** и **shutdown**
- Можно делать асинхронные операции до и после `yield`
- Все ресурсы должны закрываться после `yield`

---

## 2. Подключение к FastAPI

```python
app = FastAPI(lifespan=lifespan)
```

Теперь при запуске:
- выполняется код **до yield**
- после остановки сервера — код **после yield**

---

## 3. Пример: обновление базы без Alembic

Если не используем Alembic, можно создать/обновить таблицы **автоматически** через SQLAlchemy 2.0:

```python
from sqlalchemy.ext.asyncio import create_async_engine
from app.modules.models import Base

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/mydb"
engine = create_async_engine(DATABASE_URL, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting application...")

    # Создаём или обновляем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    print("🛑 Shutting down application...")
```

- `run_sync(Base.metadata.create_all)` — запускает **создание таблиц синхронно в async контексте**
- Можно добавить любые **seed-данные** перед `yield`

---

## 4. Добавление сидов (необязательно)

```python
async def run_seeds(session):
    from app.modules.repositories import UserRepository
    repo = UserRepository(session)
    await repo.create(username="alice", email="alice@test.com")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting application...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Сессия для сидов
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import async_sessionmaker

    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with async_session() as session:
        await run_seeds(session)

    yield

    print("🛑 Shutting down application...")
```

---

## 5. Советы

- **Не смешивать sync и async** — используйте только async engine и sessions
- **run_sync()** полезен для операций, которые в SQLAlchemy ещё sync
- Для больших проектов лучше всё же **Alembic**, но для тестов и локальной разработки такой подход работает
- Любые внешние сервисы (Redis, Kafka, S3) тоже удобно инициализировать в lifespan

---

💡 Итого:

- `@asynccontextmanager` = современный lifecycle FastAPI  
- `yield` делит startup и shutdown  
- `run_sync(Base.metadata.create_all)` = обновление базы без Alembic  
- `__init__.py` — удобный способ автоматической регистрации моделей
- Можно добавлять сиды и другие ресурсы
```
