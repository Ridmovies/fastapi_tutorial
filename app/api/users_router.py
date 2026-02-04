from fastapi import APIRouter
from sqlalchemy import select

from app.core.database import DBSession
from app.models import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_all_users(
        session: DBSession
):
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()