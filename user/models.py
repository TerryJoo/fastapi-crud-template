from datetime import datetime

from sqlalchemy import Column, Integer, String, Engine, func, DateTime
from sqlalchemy.orm import declarative_base

UserDB = declarative_base()


class User(UserDB):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    email = Column(String(320), nullable=True)
    password = Column(String(128), nullable=True)
    created_at: datetime = Column(DateTime, default=func.now(), server_default=func.now())
    updated_at: datetime = Column(String(50), default=func.now(), server_default=func.now(), onupdate=func.now())

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, created_at={self.created_at}, updated_at={self.updated_at})"


def init_db(engine: Engine):
    UserDB.metadata.create_all(bind=engine)
