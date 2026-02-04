# app/modules/__init__.py
# Импортируем все модели, чтобы Base.metadata их видел
from app.models.user import User

__all__ = ["User"]




