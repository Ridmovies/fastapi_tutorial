from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import DBSession
from app.models import User
from app.schemas.user import UserCreate, UserWithProfileRead

router = APIRouter(prefix="/users", tags=["users"])

@router.get("")
async def get_all_users(
        session: DBSession
):
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.post("")
async def create_user(
        session: DBSession,
        user_data: UserCreate,
):
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    return user


@router.get("/{user_id}", response_model=UserWithProfileRead)
async def get_user_by_id(
        session: DBSession,
        user_id: int
):
    stmt = (
        select(User)
        .options(selectinload(User.profile))
        .where(User.id == user_id))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

