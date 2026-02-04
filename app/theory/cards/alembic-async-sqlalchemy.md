```
# Alembic для асинхронной БД (SQLAlchemy 2.0+)

Эта карточка показывает, как быстро подключить Alembic для **async engine** (например, PostgreSQL + asyncpg).

---

## 1️⃣ Установка

```bash
pip install alembic psycopg2-binary
```

- `alembic` — инструмент миграций
- `psycopg2-binary` — драйвер PostgreSQL (для Alembic можно использовать sync driver)
- Для async SQLAlchemy используем `asyncpg` в проекте, Alembic работает через sync обёртку.

---

## 2️⃣ Инициализация Alembic с async шаблоном

```bash
alembic init --template async alembic
```

- Создаёт папку `alembic/` с шаблоном для асинхронной БД
- Создаёт `alembic.ini` для конфигурации

> Проверить доступные шаблоны:
>
> ```bash
> alembic list_templates
> ```

---

## 3️⃣ Настройка `alembic.ini`

```ini
sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/mydb
```

- Указываем **async драйвер** для работы в проекте
- Alembic будет использовать sync engine при генерации миграций, но ORM-сессии остаются async

---

## 4️⃣ Настройка `env.py` для async

```python
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.core.database import Base  # Ваш Base с mapped models

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Async engine
connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

async def run_migrations_online():
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
```

- `Base.metadata` содержит все модели
- `run_sync` позволяет Alembic работать через async engine

---

## 5️⃣ Генерация миграции

```bash
alembic revision --autogenerate -m "Initial async migration"
```

- Alembic сравнивает `metadata` моделей с текущей БД
- Генерирует SQL для создания таблиц

---

## 6️⃣ Применение миграций

```bash
alembic upgrade head
```

- Применяет все миграции до последней
- Работает с async engine через sync bridge

---

## ✅ Быстрый чеклист

1. `pip install alembic psycopg2-binary`
2. `alembic init --template async alembic`
3. Указать `sqlalchemy.url` с async драйвером
4. Подключить `Base.metadata` в `env.py`
5. `alembic revision --autogenerate -m "init"`
6. `alembic upgrade head`

> Всё готово! Миграции теперь работают с async SQLAlchemy 2.0+.

```
