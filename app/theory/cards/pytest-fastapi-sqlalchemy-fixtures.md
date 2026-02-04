```
# Pytest для FastAPI + SQLAlchemy 2.0+ (с async фикстурами)

Эта карточка показывает, как настроить pytest для **асинхронного FastAPI проекта** с современным SQLAlchemy 2.0, используя **async_sessionmaker** и фикстуры.

---

## 1️⃣ Установка зависимостей

```bash
pip install pytest pytest-asyncio httpx
```

- `pytest` — тестовый раннер
- `pytest-asyncio` — поддержка async/await
- `httpx` — асинхронный клиент для тестирования FastAPI

---

## 2️⃣ Структура проекта

```
app/
  main.py
  modules/
    __init__.py
    user.py
    workout.py
tests/
  conftest.py
  test_users.py
```

- `conftest.py` — глобальные фикстуры для DB и клиента
- `test_*.py` — тестовые модули

---

## 3️⃣ Фикстуры conftest.py

```python
import pytest
from httpx import AsyncClient
from app.main import app
from app.core.database import engine, AsyncSessionTest, Base

# -------------------------------------------------
# Фикстура: создаём и очищаем базу перед сессией
# -------------------------------------------------
@pytest.fixture(scope="session")
async def setup_db():
    # создаём таблицы (drop_all для dev)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # удаляем таблицы после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# -------------------------------------------------
# Фикстура: отдельная сессия на каждый тест
# -------------------------------------------------
@pytest.fixture
async def db_session(setup_db):
    async with AsyncSessionTest() as session:
        yield session
        await session.rollback()  # чистим данные после каждого теста

# -------------------------------------------------
# Фикстура: асинхронный тест-клиент FastAPI
# -------------------------------------------------
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

**Объяснения:**

- `setup_db` — создаёт таблицы один раз для всей сессии тестов, затем очищает их после завершения
- `db_session` — даёт каждому тесту **чистую сессию**, rollback откатывает все изменения
- `async_client` — асинхронный HTTP клиент для тестирования FastAPI endpoints
- Все фикстуры используют `async`/`await`, совместимо с SQLAlchemy 2.0+ и async engine

---

## 4️⃣ Пример теста с фикстурами

```python
import pytest
from app.modules.repositories import UserRepository

@pytest.mark.asyncio
async def test_create_user(db_session):
    repo = UserRepository(session=db_session)
    user = await repo.create(username="alice", email="alice@test.com")

    assert user.id is not None
    assert user.username == "alice"

@pytest.mark.asyncio
async def test_check_endpoint(async_client):
    response = await async_client.get("/dev/check-database")
    assert response.status_code == 200
```

**Объяснения:**

- `@pytest.mark.asyncio` нужен для асинхронных тестов
- `db_session` обеспечивает чистую базу для каждого теста
- `async_client` позволяет тестировать реальные HTTP endpoints
- Все изменения в базе откатываются автоматически после каждого теста

---

## 5️⃣ Почему это важно

- **Изоляция тестов**: rollback каждой сессии предотвращает загрязнение данных
- **Повторяемость**: тесты можно запускать многократно без вмешательства вручную
- **Совместимость с async**: современный SQLAlchemy 2.0 + FastAPI async
- **Подготовка CI/CD**: эти фикстуры можно использовать прямо в pipeline

---

## 6️⃣ Советы и best practices

1. **Использовать отдельную тестовую базу** (`postgresql+asyncpg://user:pass@localhost:5432/test_db`)
2. **Импортировать все модели через `__init__.py`** чтобы `Base.metadata.create_all()` видел все таблицы
3. **Использовать async_sessionmaker** для корректной работы async SQLAlchemy
4. **Rollback после каждого теста** — гарантирует чистую среду
5. **Тестировать endpoints через AsyncClient** — реально запускает код FastAPI
6. Для проверки deprecated кода можно добавить **AST-тесты** или mypy-тесты отдельно

---

💡 Итог:

- `setup_db` = создание/очистка таблиц
- `db_session` = чистая сессия для каждого теста
- `async_client` = асинхронный HTTP-клиент
- Всё вместе даёт современный workflow для FastAPI + SQLAlchemy 2.0+ в pytest
```
