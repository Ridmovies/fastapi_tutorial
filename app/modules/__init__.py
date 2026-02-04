# app/modules/__init__.py
# Импортируем все модели, чтобы Base.metadata их видел


__all__ = ["User", "Workout"]

from app.modules.deprecated import User, Workout
