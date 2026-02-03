# SQLAlchemy Mapped модели: Поля и параметры

В SQLAlchemy 2.0+ используется стиль `Mapped` для описания колонок с аннотацией типов.  
Это современный способ, который позволяет IDE видеть типы и улучшает автокомплит и проверку типов.

---

## Примеры полей

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Float, DateTime, Text, ForeignKey
from datetime import datetime, timezone

    class User(Base):
        __tablename__ = "users"

        id: Mapped[int] = mapped_column(primary_key=True)               # первичный ключ
        username: Mapped[str] = mapped_column(String, unique=True)     # уникальная строка
        email: Mapped[str] = mapped_column(String, index=True)         # индексированная строка
        age: Mapped[int] = mapped_column(default=18)                   # integer с дефолтом
        is_active: Mapped[bool] = mapped_column(default=True)          # boolean
        balance: Mapped[float] = mapped_column(default=0.0)            # float
        bio: Mapped[str] = mapped_column(Text, nullable=True)          # текстовое поле, может быть null
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
        )  # дата/время с таймзоной
        team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))   # внешний ключ на другую таблицу

---

## Основные параметры mapped_column

- primary_key=True — колонка является первичным ключом
- unique=True — уникальные значения
- index=True — создаёт индекс
- default=value / default=lambda: ... — значение по умолчанию
- nullable=True/False — разрешено ли значение NULL
- ForeignKey("table.column") — ссылка на другую таблицу
- autoincrement=True — автоинкремент для integer
- onupdate=func — функция для автоматического обновления (например, timestamp)

---

## Типы полей (Mapped[Type])

- int / Integer
- str / String / Text
- bool / Boolean
- float / Float / Numeric
- datetime / DateTime
- date / Date
- time / Time
- Enum / JSON / LargeBinary и др.

---

## Связи (Relationships)

- Одно-к-одному: `relationship("OtherModel", uselist=False)`
- Один-ко-многим: `relationship("OtherModel", back_populates="parent")`
- Многие-ко-многим: через вспомогательную таблицу
- Важно использовать `Mapped[List[OtherModel]]` для коллекций

---

💡 Запомнить легко:  
`Mapped[Type] = mapped_column(...)` = колонка с **типом Python** + SQLAlchemy опциями.  
Связи и коллекции также аннотируются через `Mapped` для корректной типизации.

