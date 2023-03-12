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
