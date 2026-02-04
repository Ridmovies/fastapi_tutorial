```
# SQLAlchemy 2.0+: Связи между таблицами

В SQLAlchemy для моделирования отношений между таблицами используют **relationship** и внешние ключи (**ForeignKey**).  
Основные типы связей:

---

## 1️⃣ One-to-Many (Один-ко-многим)

- Один объект родителя связан с **несколькими объектами детей**.
- Пример: `User` имеет много `Workout`.

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    # Один пользователь -> много тренировок
    workouts: Mapped[list["Workout"]] = relationship(back_populates="user")


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    # Каждая тренировка принадлежит одному пользователю
    user: Mapped["User"] = relationship(back_populates="workouts")
```

- `ForeignKey("users.id")` — столбец в `Workout`, указывающий на `User`.
- `relationship(back_populates=...)` — связывает ORM объекты для удобного доступа.

---

## 2️⃣ One-to-One (Один-к-одному)

- Каждый объект родителя связан ровно с одним объектом ребенка.
- Пример: `User` имеет **один профиль**.

```python
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    bio: Mapped[str] = mapped_column(default="")

    user: Mapped["User"] = relationship(back_populates="profile")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)

    profile: Mapped["UserProfile"] = relationship(back_populates="user", uselist=False)
```

- `uselist=False` говорит SQLAlchemy, что это **один объект**, а не список.
- `unique=True` на ForeignKey обеспечивает уникальность в базе.

---

## 3️⃣ Many-to-Many (Многие-ко-многим)

- Объекты обеих таблиц могут иметь несколько связей.
- Нужна **таблица-связка (association table)**.

```python
from sqlalchemy import Table

user_workout_association = Table(
    "user_workout_association",
    Base.metadata,
    mapped_column("user_id", ForeignKey("users.id"), primary_key=True),
    mapped_column("workout_id", ForeignKey("workouts.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)

    workouts: Mapped[list["Workout"]] = relationship(
        secondary=user_workout_association,
        back_populates="users"
    )

class Workout(Base):
    __tablename__ = "workouts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()

    users: Mapped[list["User"]] = relationship(
        secondary=user_workout_association,
        back_populates="workouts"
    )
```

- `secondary` — ссылка на таблицу-связку.
- `back_populates` — двусторонняя связь, ORM автоматически синхронизирует списки.

---

## 4️⃣ Резюме

| Тип связи | Пример | Ключевые моменты |
|-----------|--------|-----------------|
| One-to-Many | User → Workout | ForeignKey в дочерней таблице, relationship(list) |
| One-to-One | User → UserProfile | uselist=False, unique=True |
| Many-to-Many | User ↔ Workout | Таблица-связка + secondary |

---

💡 Советы:

1. Всегда указывай `back_populates`, чтобы связь была двусторонней.
2. Для One-to-One обязательно `uselist=False`.
3. Для Many-to-Many нужен `secondary` с таблицей-связкой.
4. Используй **Mapped** и `mapped_column` в стиле SQLAlchemy 2.0+.
5. Для списков используем тип `Mapped[list[Type]]`.

```
