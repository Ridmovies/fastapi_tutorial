import pytest


@pytest.mark.asyncio
async def test_connect_db(async_client):
    response = await async_client.get("/dev/check-database")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user(async_client):
    user_json = {"username": "test"}
    response = await async_client.post("/users", json=user_json)
    assert response.status_code == 200