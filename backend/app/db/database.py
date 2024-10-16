from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings


DATABASE_URL = settings.POSTGRES_DSN

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
