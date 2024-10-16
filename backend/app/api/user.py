from typing import List, Dict
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.user import User
from app.services.user import UserService
from app.schemas.user import (
    UserResponse,
    TokenResponse,
    SignUpRequest,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    RefreshAccessTokenRequest,
)

user_router = APIRouter()


@user_router.get(
    "/user_by_id",
    summary="Get User By Id",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def user_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(UserService.authenticate_current_user),
) -> UserResponse:
    response = await UserService.get_user_by_id(id=id, db=db)
    return response


@user_router.get(
    "/user_by_email",
    summary="Get User By Email",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(UserService.authenticate_current_user),
) -> UserResponse:
    response = await UserService.get_user_by_email(email=email, db=db)
    return response


@user_router.get(
    "/users",
    summary="Get All Users",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def users(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(UserService.authenticate_current_user),
) -> List[UserResponse]:
    response = await UserService.get_all_users(db=db)
    return response


@user_router.post(
    "/refresh_token",
    summary="Refresh Token",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def refresh_token(
    data: RefreshAccessTokenRequest, db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    response = await UserService.refresh_access_token(
        refresh_token=data.refresh_token, db=db
    )
    return response


@user_router.post(
    "/authorize",
    summary="Create Access And Refresh Tokens For User",
    status_code=status.HTTP_201_CREATED,
)
async def authorize(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    user = await UserService.authenticate(
        email=form_data.username, password=form_data.password, db=db
    )
    response = UserService.create_access_token(user.id, expires_delta=None)
    return {"access_token": response["encoded_jwt"]}


@user_router.post(
    "/current_authenticated_user",
    summary="Get Current Authenticated User",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def current_authenticated_user(
    user: LoginRequest = Depends(UserService.authenticate_current_user),
) -> UserResponse:
    return user


@user_router.post(
    "/signup",
    summary="SignUp",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    data: SignUpRequest, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    response = await UserService.signup_user(data=data, db=db)
    return response


@user_router.post(
    "/login",
    summary="Login",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def login(
    data: LoginRequest, db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    response = await UserService.login_user(data=data, db=db)
    return response


@user_router.post(
    "/forgot_password",
    summary="Forgot Password",
    status_code=status.HTTP_201_CREATED,
)
async def forgot_password(
    data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    response = await UserService.forgot_user_password(data=data, db=db)
    return response


@user_router.put(
    "/reset_password",
    summary="Reset Password",
    status_code=status.HTTP_201_CREATED,
)
async def reset_password(
    data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    response = await UserService.reset_user_password(data=data, db=db)
    return response
