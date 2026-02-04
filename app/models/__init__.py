# app/modules/__init__.py
# Импортируем все модели, чтобы Base.metadata их видел
from app.models.user import User, UserProfile

__all__ = ["User", "UserProfile"]




