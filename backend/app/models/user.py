from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import EmailStr
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    date_created: Mapped[datetime] = mapped_column(default=datetime.utcnow)
