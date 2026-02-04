"""
LEGACY MODULE (SQLAlchemy < 2.0)

⚠️ Этот файл содержит УСТАРЕВШИЙ стиль:
- declarative_base()
- Column(...)
- session.query()
- sync engine / session
- отсутствие type hints
- datetime без timezone
- implicit magic

Использовать ТОЛЬКО для тестов, линтеров и миграций.
"""

from datetime import datetime

from fastapi import APIRouter
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from app.core.database import DATABASE_URL, Base


# ---------------------------------------------------------------------
# BASE (deprecated)
# ---------------------------------------------------------------------

# Base = declarative_base()


# ---------------------------------------------------------------------
# MODELS (deprecated)
# ---------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    workouts = relationship("Workout", back_populates="user")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workouts")


# ---------------------------------------------------------------------
# ENGINE & SESSION (deprecated)
# ---------------------------------------------------------------------

engine = create_engine(
    # "postgresql://user:password@localhost:5432/legacy_db",
    DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ---------------------------------------------------------------------
# REPOSITORY (deprecated)
# ---------------------------------------------------------------------

class UserRepository:
    """
    Устаревший репозиторий:
    - session.query()
    - implicit commits
    - no context manager
    """

    def __init__(self):
        self.db = SessionLocal()

    def get_by_id(self, user_id: int):
        return (
            self.db
            .query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_by_username(self, username: str):
        return (
            self.db
            .query(User)
            .filter(User.username == username)
            .first()
        )

    def get_all(self):
        return self.db.query(User).all()

    def create(self, username: str, email: str | None = None):
        user = User(username=username, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int):
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
        return user


class WorkoutRepository:
    """
    Ещё больше legacy:
    - join через relationship implicitly
    """

    def __init__(self):
        self.db = SessionLocal()

    def get_user_workouts(self, user_id: int):
        return (
            self.db
            .query(Workout)
            .filter(Workout.user_id == user_id)
            .all()
        )

    def create(self, user_id: int, title: str):
        workout = Workout(user_id=user_id, title=title)
        self.db.add(workout)
        self.db.commit()
        self.db.refresh(workout)
        return workout


