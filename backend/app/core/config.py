import os
import logging
import asyncio
from typing import List, ClassVar
from dotenv import load_dotenv
from pydantic import AnyHttpUrl, computed_field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis import Redis
from celery import Celery
from celery.utils.log import get_task_logger


class Settings(BaseSettings):
    load_dotenv()

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"), case_sensitive=True
    )
    # `.env.prod` takes priority over `.env`

    ENV: str = os.getenv("ENV", "dev")

    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    PROJECT_NAME: str = "Fast-Api-PostGres-BoilerPlate"

    DATABASE_SCHEME: str = os.environ["DATABASE_SCHEME"]
    POSTGRES_DB_NAME: str = os.environ["POSTGRES_DB_NAME"]
    POSTGRES_USER: str = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_HOST: str = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT: int = os.environ["POSTGRES_PORT"]
    MAX_CONNECTIONS_COUNT: int = os.environ["MAX_CONNECTIONS_COUNT"]
    MIN_CONNECTIONS_COUNT: int = os.environ["MIN_CONNECTIONS_COUNT"]

    JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
    TOKEN_ALGORITHM: str = os.environ["TOKEN_ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.environ["REFRESH_TOKEN_EXPIRE_MINUTES"]
    RESET_TOKEN_EXPIRE_MINUTES: int = os.environ["RESET_TOKEN_EXPIRE_MINUTES"]

    EMAIL_HOST: str = os.environ["EMAIL_HOST"]
    EMAIL_PORT: int = os.environ["EMAIL_PORT"]
    EMAIL_USER: str = os.environ["EMAIL_USER"]
    EMAIL_PASSWORD: str = os.environ["EMAIL_PASSWORD"]

    REDIS_URL: str = os.environ["REDIS_URL"]
    CELERY_BROKER_URL: str = os.environ["CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND: str = os.environ["CELERY_RESULT_BACKEND"]
    

    logger: ClassVar[logging.Logger] = get_task_logger(__name__)

    loop: ClassVar[asyncio.AbstractEventLoop] = asyncio.get_event_loop()

    redis_client: ClassVar[Redis] = Redis.from_url(CELERY_BROKER_URL)

    celery: ClassVar[Celery] = Celery(__name__)
    celery.conf.broker_url = CELERY_BROKER_URL
    celery.conf.result_backend = CELERY_RESULT_BACKEND
    celery.conf.broker_connection_retry_on_startup = True
    celery.conf.task_track_started = True
    celery.conf.task_ignore_result = False

    @computed_field
    @property
    def POSTGRES_DSN(self) -> PostgresDsn:
        return str(
            PostgresDsn.build(
                scheme=self.DATABASE_SCHEME,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=f"{self.POSTGRES_DB_NAME}",
            )
        )


settings = Settings()
