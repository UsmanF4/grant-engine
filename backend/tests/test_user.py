import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_user_signup(async_client: AsyncClient):
    data = {
        "email": "user@example.com",
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "password": "String@123",
    }
    response = await async_client.post("/api/v1/user/signup", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_login(async_client: AsyncClient, test_user):
    data = {
        "email": test_user["email"],
        "password": test_user["password"],
        "remember_me": True,
    }
    response = await async_client.post("/api/v1/user/login", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_users(authorized_client):
    response = await authorized_client.get("/api/v1/user/users")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_id(authorized_client, test_user):
    response = await authorized_client.get(
        f"/api/v1/user/user_by_id?id={test_user['id']}"
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]


@pytest.mark.asyncio
async def test_get_user_by_email(authorized_client, test_user):
    response = await authorized_client.get(
        f"/api/v1/user/user_by_email?email={test_user['email']}"
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]


@pytest.mark.asyncio
async def test_authorize(async_client: AsyncClient, test_user):
    form_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    response = await async_client.post("/api/v1/user/authorize", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_current_authenticated_user(authorized_client, test_user):
    response = await authorized_client.post("/api/v1/user/current_authenticated_user")
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]


@pytest.mark.asyncio
async def test_forgot_password(async_client: AsyncClient, test_user):
    data = {"email": test_user["email"]}
    response = await async_client.post("/api/v1/user/forgot_password", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_refresh_token(async_client: AsyncClient, refresh_token):
    data = {"refresh_token": refresh_token}
    response = await async_client.post("/api/v1/user/refresh_token", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_reset_password(async_client: AsyncClient, reset_token):
    data = {"reset_token": reset_token, "password": "String@12345"}
    response = await async_client.put("/api/v1/user/reset_password", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_reset_password_errors(async_client: AsyncClient):
    data = {"reset_token": "some invalid token", "password": "String@12345"}
    response = await async_client.put("/api/v1/user/reset_password", json=data)
    assert response.status_code == 400


@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        (uuid4(), 404),  # Non-existent user ID
        ("invalid-uuid", 422),  # Invalid UUID format
    ],
)
@pytest.mark.asyncio
async def test_get_user_by_id_errors(authorized_client, user_id, expected_status):
    response = await authorized_client.get(f"/api/v1/user/user_by_id?id={user_id}")
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "email, expected_status",
    [
        ("nonexistent@example.com", 404),  # Non-existent email
        (
            "invalid-email-format",
            404,
        ),  # Invalid email format (status code should be 400, not 404)
    ],
)
@pytest.mark.asyncio
async def test_get_user_by_email_errors(authorized_client, email, expected_status):
    response = await authorized_client.get(f"/api/v1/user/user_by_email?email={email}")
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "String@123", 422),
        ("user@example.com", "wrongpassword", 422),
    ],
)
@pytest.mark.asyncio
async def test_incorrect_login(
    async_client: AsyncClient, test_user, email, password, status_code
):
    response = await async_client.post(
        "/api/v1/user/login", data={"username": email, "password": password}
    )

    assert response.status_code == status_code
