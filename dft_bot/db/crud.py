from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import os
from dft_bot.db.models import Base, User, UserTypeEnum

engine = create_engine(os.environ.get("DATABASE_PATH", "sqlite:///./dft.db"))


def init_db():
    Base.metadata.create_all(engine)


def insert_active_user(_id: str, user_type: UserTypeEnum):
    with Session(engine) as session:
        if get_user(_id, user_type, session):
            return
        u = User(id=_id, user_type=user_type, active=True)
        session.add(u)
        session.commit()


def get_user(_id: str, user_type: UserTypeEnum, session: Session = None):
    if not session:
        session = Session(engine)
    return (
        session.query(User).where(User.id == _id, User.user_type == user_type).first()
    )


def is_user_active(_id: str, user_type: UserTypeEnum, session: Session = None):
    if user := get_user(_id, user_type, session):
        return user.active
    return False
