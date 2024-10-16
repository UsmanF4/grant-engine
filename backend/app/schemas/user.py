from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserBaseExtended(UserBase):
    username: str
    first_name: str
    last_name: str


class UserResponse(UserBaseExtended):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SignUpRequest(UserBaseExtended):
    password: str

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(UserBase):
    password: str
    remember_me: bool

    model_config = ConfigDict(from_attributes=True)


class ForgotPasswordRequest(UserBase):

    model_config = ConfigDict(from_attributes=True)


class ResetPasswordRequest(BaseModel):
    reset_token: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenRequest(BaseModel):
    sub: UUID
    exp: int

    model_config = ConfigDict(from_attributes=True)


class RefreshAccessTokenRequest(BaseModel):
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)
