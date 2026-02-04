```
# SQLAlchemy 2.0+: отличия от старых версий (что изменилось навсегда)

SQLAlchemy 2.0 — это не просто апдейт, а смена парадигмы.
Многие старые подходы считаются устаревшими или deprecated.

---

## 1. Декларативные модели

### ❌ Было (старый стиль)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)

### ✅ Стало (SQLAlchemy 2.0+)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()

📌 Почему:
- Полная поддержка type hints
- IDE и линтеры понимают модель
- Старый стиль считается legacy

---

## 2. Колонки: Column vs Mapped

### ❌ Было

username = Column(String, unique=True)

### ✅ Стало

username: Mapped[str] = mapped_column(unique=True)

📌 Изменение:
- Column больше не рекомендуется
- Mapped + mapped_column — стандарт 2.0

---

## 3. Session и работа с БД

### ❌ Было

db.query(User).filter(User.id == user_id).first()

### ✅ Стало

stmt = select(User).where(User.id == user_id)
result = await session.execute(stmt)
user = result.scalar_one_or_none()

📌 Почему:
- query() считается legacy API
- select() — единый стиль для sync и async

---

## 4. Асинхронность — first-class citizen

### ❌ Было (или вообще отсутствовало)

sessionmaker(bind=engine)

### ✅ Стало

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

📌 Важно:
- async_sessionmaker — стандарт
- async/await везде
- asyncpg — рекомендуемый драйвер для Postgres

---

## 5. DeclarativeBase вместо declarative_base

### ❌ Было

Base = declarative_base()

### ✅ Стало

class Base(DeclarativeBase):
    pass

📌 Плюсы:
- Можно добавлять общие поля и методы
- Лучшая типизация
- Чистая архитектура

---

## 6. Отношения (relationship)

### ❌ Было

workouts = relationship("Workout")

### ✅ Стало

workouts: Mapped[list["Workout"]] = relationship(back_populates="user")

📌 Почему:
- Коллекции тоже типизируются
- Явно видно: список, один объект, optional

---

## 7. Nullable и Optional

### ❌ Было

name = Column(String, nullable=True)

### ✅ Стало

name: Mapped[str | None] = mapped_column(nullable=True)

📌 Правило:
- Python-тип отражает nullable
- IDE сразу показывает возможный None

---

## 8. DateTime и timezone

### ❌ Было

created_at = Column(DateTime, default=datetime.utcnow)

### ✅ Стало

created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc)
)

📌 Почему:
- utcnow() без timezone — плохо
- SQLAlchemy 2.0 поощряет timezone-aware даты

---

## 9. Явность — главный принцип 2.0

SQLAlchemy 2.0 требует:
- явных типов
- явных select()
- явных async/sync границ
- минимальной магии

Это делает код:
- предсказуемым
- читаемым
- безопасным для больших проектов

---

## Итоговое правило

❗ Всё, что выглядит так, как будто написано в 2019 году — скорее всего legacy.

✅ Современный стек SQLAlchemy 2.0+:
- DeclarativeBase
- Mapped / mapped_column
- select()
- async_sessionmaker
- asyncpg
- строгая типизация

---

💡 Если сомневаешься — спроси себя:
"Это выглядит как типизированный Python?"
Если нет — скорее всего это старый стиль.
```
