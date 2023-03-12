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
                           update_schema=V1UserUpdateDto),
    UserService)

