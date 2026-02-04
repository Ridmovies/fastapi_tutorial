import pytest

from app.modules.deprecated import UserRepository
from app.modules import User
from app.modules import Workout

@pytest.mark.asyncio
async def test_connect_db(async_client):
    response = await async_client.get("/dev/check-database")
    assert response.status_code == 200