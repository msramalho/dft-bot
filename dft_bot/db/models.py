from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import enum


class Base(DeclarativeBase):
    pass


class UserTypeEnum(enum.Enum):
    telegram = 1


class User(Base):
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(primary_key=True)
    user_type: Mapped[str] = mapped_column(
        Enum(UserTypeEnum), primary_key=True
    )  # telegram, discord, ...
    active: Mapped[bool] = mapped_column(default=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
