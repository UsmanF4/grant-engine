import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ping(async_client: AsyncClient):
    response = await async_client.get("/ping")
    assert response.json() == "Pong!"
    assert response.status_code == 200
