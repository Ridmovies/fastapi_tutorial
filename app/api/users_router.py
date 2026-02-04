from fastapi import APIRouter
from sqlalchemy import select

from app.core.database import DBSession
from app.models import User
from app.schemas import UserCreate

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

