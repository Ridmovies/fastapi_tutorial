# Pydantic схемы в FastAPI

**Pydantic** — библиотека для валидации и сериализации данных.  
FastAPI использует Pydantic для:

- проверки входящих данных
- формирования ответов
- автогенерации документации (Swagger / OpenAPI)

---

## Зачем нужны Pydantic схемы

Без схем мы работаем с `dict`, что:

- небезопасно
- неудобно
- плохо документируется

Pydantic решает все эти проблемы.

---

## Простейшая схема

    from pydantic import BaseModel

    class User(BaseModel):
        id: int
        name: str
        email: str

FastAPI автоматически:
- проверит типы
- вернёт ошибку 422 при неверных данных
- отобразит схему в Swagger

---

## Использование в POST-запросе

    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI()

    class UserCreate(BaseModel):
        name: str
        email: str

    @app.post("/users")
    def create_user(user: UserCreate):
        return user

FastAPI:
- читает JSON из body
- валидирует данные
- передаёт объект `UserCreate` в функцию

---

## Разделение схем (Best Practice)

Обычно создают несколько схем:

    class UserBase(BaseModel):
        name: str
        email: str


    class UserCreate(UserBase):
        password: str


    class UserRead(UserBase):
        id: int

Почему так:

- `UserCreate` — входящие данные
- `UserRead` — данные для ответа
- пароль никогда не возвращается клиенту

---

## response_model

    @app.get("/users/{user_id}", response_model=UserRead)
    def get_user(user_id: int):
        return {
            "id": user_id,
            "name": "John",
            "email": "john@example.com",
            "password": "secret"
        }

Даже если `password` есть в данных —  
**в ответе его не будет**.

---

## Валидация полей

    from pydantic import Field

    class Product(BaseModel):
        name: str = Field(min_length=3, max_length=100)
        price: float = Field(gt=0)

Ошибки автоматически превращаются в `422 Unprocessable Entity`.

---

## Опциональные поля

    from typing import Optional

    class UserUpdate(BaseModel):
        name: Optional[str] = None
        email: Optional[str] = None

Используется для `PATCH` и `PUT`.

---

## ORM Mode (SQLAlchemy)
В Pydantic v2 используется model_config

    from pydantic import BaseModel
    from pydantic import ConfigDict
    
    
    class UserRead(BaseModel):
        id: int
        name: str
    
        model_config = ConfigDict(from_attributes=True)

Позволяет возвращать **ORM-объекты**, а не словари.

---

## Частые ошибки новичков

- Использовать одну схему для всего
- Возвращать пароль в ответе
- Делать валидацию вручную
- Не использовать `response_model`

---

## Итог

Pydantic схемы дают:

- безопасные входные данные
- чистые ответы
- автодокументацию
- поддерживаемый код

Если вы используете FastAPI — **Pydantic обязателен**.
