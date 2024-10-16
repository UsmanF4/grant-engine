import re
import smtplib
from typing import Optional, Union, Any, Dict, List
from datetime import datetime, timedelta
from pytz import timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserResponse,
    LoginRequest,
    SignUpRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    TokenRequest,
    TokenResponse,
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        try:
            verification = password_context.verify(password, hashed_password)
            return verification

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    def validate_password(password: str) -> None:
        try:
            password_regex = r"^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$"

            if not re.match(password_regex, password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password must contain at least 1 digit, 1 lowercase letter, 1 uppercase letter, 1 special character, and be at least 8 characters long",
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    def get_password(password: str) -> str:
        try:
            password = password_context.hash(password)
            return password

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def update_user_password(
        id: int, password: str, db: AsyncSession
    ) -> Optional[User]:
        try:
            user = await UserService.get_user_by_id(id=id, db=db)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User does not exist",
                )
            user.password = UserService.get_password(password=password)
            await db.commit()
            return user

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def get_user_by_id(id: int, db: AsyncSession) -> UserResponse:
        try:
            result = await db.execute(select(User).where(User.id == id))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession) -> UserResponse:
        try:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def get_all_users(db: AsyncSession) -> List[UserResponse]:
        try:
            result = await db.execute(select(User))
            users = result.scalars().all()
            return users

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def check_existing_email(email: str, db: AsyncSession) -> None:
        try:
            result = await db.execute(select(User).where(User.email == email))
            existing_user = result.scalars().first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists. Please use a different email address.",
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def authenticate(
        email: str, password: str, db: AsyncSession
    ) -> Optional[User]:
        try:
            user = await UserService.get_user_by_email(email=email, db=db)
            if not user or not UserService.verify_password(
                password=password, hashed_password=user.password
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return user

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    def verify_and_decode_token(token: str) -> TokenRequest:
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM]
            )
            return TokenRequest(**payload)

        except (JWTError, ValidationError) as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could Not Validate Credentials",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e

    @staticmethod
    def validate_token_expiry(token_data: TokenRequest) -> None:
        try:
            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token Expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def authenticate_current_user(
        token: str = Depends(
            OAuth2PasswordBearer(
                tokenUrl=f"{settings.API_V1_STR}/user/authorize", scheme_name="JWT"
            )
        ),
        db: AsyncSession = Depends(get_db),
    ) -> User:
        try:
            token_data = UserService.verify_and_decode_token(token=token)
            UserService.validate_token_expiry(token_data=token_data)
            user = await UserService.get_user_by_id(token_data.sub, db=db)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Could Not Find User"
                )
            return user

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could Not Validate Credentials",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e

    @staticmethod
    def create_access_token(
        subject: Union[str, Any], expires_delta: Union[int, None] = None
    ) -> Dict[str, Any]:
        try:
            if expires_delta is None:
                expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            elif expires_delta == "remember_me":
                expires_delta = timedelta(days=7)

            expires_at = timezone("UTC").localize(datetime.utcnow() + expires_delta)
            to_encode = {"exp": expires_at, "sub": str(subject)}
            encoded_jwt = jwt.encode(
                to_encode, settings.JWT_SECRET_KEY, settings.TOKEN_ALGORITHM
            )

            return {"expires_at": expires_at, "encoded_jwt": encoded_jwt}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    def create_refresh_token(
        subject: Union[str, Any], expires_delta: Union[int, None] = None
    ) -> str:
        try:
            if expires_delta is None:
                expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
            expires_at = timezone("UTC").localize(datetime.utcnow() + expires_delta)
            to_encode = {"exp": expires_at, "sub": str(subject)}
            encoded_jwt = jwt.encode(
                to_encode, settings.JWT_SECRET_KEY, settings.TOKEN_ALGORITHM
            )
            return encoded_jwt

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    def create_reset_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        try:
            if expires_delta is None:
                expires_delta = timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES)
            expires_at = timezone("UTC").localize(datetime.utcnow() + expires_delta)
            to_encode = {"exp": expires_at, "sub": str(subject)}
            encoded_jwt = jwt.encode(
                to_encode, settings.JWT_SECRET_KEY, settings.TOKEN_ALGORITHM
            )
            return encoded_jwt

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def refresh_access_token(refresh_token: str, db: AsyncSession):
        try:
            payload = jwt.decode(
                refresh_token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.TOKEN_ALGORITHM],
            )
            token_data = TokenRequest(**payload)
            user = await UserService.get_user_by_id(token_data.sub, db=db)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Invalid Token For User",
                )
            token_data = UserService.create_access_token(user.id)
            access_token = token_data["encoded_jwt"]
            refresh_token = UserService.create_refresh_token(user.id)
            expires_at = token_data["expires_at"]
            token_response = TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at,
            )
            return token_response

        except (JWTError, ValidationError) as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e

    @staticmethod
    async def signup_user(data: SignUpRequest, db: AsyncSession) -> UserResponse:
        await UserService.check_existing_email(data.email, db=db)
        UserService.validate_password(data.password)

        try:
            hashed_password = UserService.get_password(password=data.password)
            user = User(
                email=data.email,
                username=data.username,
                first_name=data.first_name,
                last_name=data.last_name,
                password=hashed_password,
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def login_user(data: LoginRequest, db: AsyncSession):
        user = await UserService.authenticate(
            email=data.email, password=data.password, db=db
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect Email Or Password",
            )

        try:
            expires_delta = "remember_me" if data.remember_me else None
            token_data = UserService.create_access_token(
                user.id, expires_delta=expires_delta
            )
            refresh_token = UserService.create_refresh_token(user.id)
            access_token = token_data["encoded_jwt"]
            expires_at = token_data["expires_at"]
            token_response = TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at,
            )
            return token_response

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def send_password_reset_email(email: str, reset_token: str):
        try:
            subject = "Password Reset Request"
            message = f"Click the following link to reset your password: http://localhost:3000/ResetPassword?resetToken={reset_token}"
            sender_email = settings.EMAIL_USER
            receiver_email = email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(sender_email, settings.EMAIL_PASSWORD)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                server.quit()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def forgot_user_password(data: ForgotPasswordRequest, db: AsyncSession):
        try:
            user = await UserService.get_user_by_email(email=data.email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Email"
                )
            reset_token = UserService.create_reset_token(user.id)
            await UserService.send_password_reset_email(
                email=user.email, reset_token=reset_token
            )
            return {
                "message": "Reset password link has been sent to your email address"
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def reset_user_password(data: ResetPasswordRequest, db: AsyncSession):
        try:
            payload = jwt.decode(
                data.reset_token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.TOKEN_ALGORITHM],
            )
            token_data = TokenRequest(**payload)
            user = await UserService.update_user_password(
                id=token_data.sub, password=data.password, db=db
            )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Invalid Token For User",
                )
            return {"message": "Password has been changed successfully."}

        except (JWTError, ValidationError) as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
