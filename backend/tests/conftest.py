import pytest_asyncio
from httpx import AsyncClient
from app.main import app
from app.core.config import settings
from app.db.database import connect_and_init_db
from app.models.user import User
from app.services.user import UserService


@pytest_asyncio.fixture(autouse=True, scope="function")
async def override_dependency():
    # db_client = AsyncMongoMockClient()[settings.MONGO_DB_NAME]

    document_models = [
        User,
       ]

    # await init_beanie(database=db_client, document_models=document_models)

    async def mock_connect_and_init_db():
        pass
        # return db_client

    app.dependency_overrides[connect_and_init_db] = mock_connect_and_init_db

    yield


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def test_user(async_client: AsyncClient):
    user_data = {
        "email": "user@example.com",
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "password": "String@123",
    }
    response = await async_client.post("/api/v1/user/signup", json=user_data)
    assert response.status_code == 200
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest_asyncio.fixture(scope="function")
async def token(test_user):
    token = UserService.create_access_token(test_user["id"], expires_delta=None)
    return token["encoded_jwt"]


@pytest_asyncio.fixture(scope="function")
async def authorized_client(async_client: AsyncClient, token):
    async_client.headers = {**async_client.headers, "Authorization": f"Bearer {token}"}
    return async_client


@pytest_asyncio.fixture(scope="function")
async def refresh_token(test_user):
    token = UserService.create_refresh_token(test_user["id"], expires_delta=None)
    return token


@pytest_asyncio.fixture(scope="function")
async def reset_token(test_user):
    token = UserService.create_reset_token(test_user["id"], expires_delta=None)
    return token
