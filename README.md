# CRUD Framework for fastapi
```python3
from crud.crud_router import create_crud_router
from crud.mapper import CRUDEntitySchemaMapper
from user import User
from user.dtos import V1UserSchema, V1UserCreateDto, V1UserUpdateDto, V1UserDetailSchema
from user.service import UserService

router = create_crud_router(
    CRUDEntitySchemaMapper(User,
                           read_schema=V1UserDetailSchema,
                           list_schema=V1UserSchema,
                           create_schema=V1UserCreateDto,
                           update_schema=V1UserUpdateDto,
                           delete_api=False,
                           # schema_entity_keys_mapping=[("api_schema_id", "db_entity_id")]
                           ),
    UserService)
```

#### User Model
```python3
from crud.crud_service import CRUDService
from user.models import User


class UserService(CRUDService[User]):
    @property
    def entity(self) -> User.__class__:
        return User
```

#### User Model
```python3
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
```
#### V1 Schema
```python3
from typing import Optional

from pydantic import BaseModel

from shared.models import TimestampModel


class V1UserSchema(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]


class V1UserDetailSchema(TimestampModel):
    id: int
    name: Optional[str]
    email: Optional[str]


class V1UserCreateDto(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]


class V1UserUpdateDto(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
```