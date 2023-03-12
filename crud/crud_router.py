from typing import Callable, Optional, Literal

from fastapi import APIRouter, Depends, Path, Body

from crud.crud_service import CRUDService
from crud.dtos import PaginationDto, PaginatedResult, APIResult, create_sort_dto
from crud.mapper import CRUDEntitySchemaMapper
from crud.types import Entity


def create_crud_router(mapper: CRUDEntitySchemaMapper, get_crud_service: Optional[Callable] = None,
                       prefix: str = None, router=APIRouter()) -> APIRouter:
    path = "/" + "/".join(filter(bool, [prefix, mapper.entity.__tablename__]))
    detail_path = "/".join(filter(bool, [path, "{" + mapper.pk_column.name + "}"]))
    if mapper.list_schema:
        register_list_api(router, path, mapper, get_crud_service)

    if mapper.read_schema:
        register_read_api(router, detail_path, mapper, get_crud_service)

    if mapper.create_schema:
        register_create_api(router, path, mapper, get_crud_service)

    if mapper.update_schema:
        register_update_api(router, detail_path, mapper, get_crud_service)

    if mapper.delete_api:
        register_delete_api(router, detail_path, mapper, get_crud_service)

    return router


def register_create_api(router: APIRouter, path: str, mapper: CRUDEntitySchemaMapper,
                        get_crud_service: Optional[Callable] = None):
    s_props_to_create = mapper.create_schema_entity_tuples
    s_props = mapper.read_schema_entity_tuples

    @router.post(path, response_model=APIResult[mapper.read_schema])
    def create(service: CRUDService[Entity] = Depends(get_crud_service), data: mapper.create_schema = Body(...)):
        data = service.create({e_k: getattr(data, s_k) for s_k, e_k in s_props_to_create if hasattr(data, s_k)})
        return APIResult(
            data=mapper.read_schema(**{s_k: getattr(data, e_k) for s_k, e_k in s_props if hasattr(data, e_k)}))


def register_list_api(router: APIRouter, path: str, mapper: CRUDEntitySchemaMapper,
                      get_crud_service: Optional[Callable] = None):
    s_props = mapper.list_schema_entity_tuples
    sort_class = create_sort_dto(s_props, mapper)

    @router.get(path, response_model=PaginatedResult[mapper.list_schema])
    def find_many(service: CRUDService[Entity] = Depends(get_crud_service),
                  sort_dto: sort_class = Depends(),
                  pagination_dto: PaginationDto = Depends()):
        data = service.find_many(**pagination_dto.to_query_dict(), order_by=sort_dto)
        result = PaginatedResult(data=[], total_count=service.count())
        for d in data:
            result.data.append(mapper.list_schema(**{s_k: getattr(d, e_k) for s_k, e_k in s_props if hasattr(d, e_k)}))
        return result


def register_read_api(router: APIRouter, path: str, mapper: CRUDEntitySchemaMapper,
                      get_crud_service: Optional[Callable] = None):
    s_props = mapper.read_schema_entity_tuples

    @router.get(path, response_model=APIResult[mapper.read_schema])
    def read(service: CRUDService[Entity] = Depends(get_crud_service),
             pk: mapper.pk_column.type.python_type = Path(..., alias=mapper.pk_column.name)):
        data = service.find_by_id(pk)
        return APIResult(
            data=mapper.read_schema(**{s_k: getattr(data, e_k) for s_k, e_k in s_props if hasattr(data, e_k)}))


def register_update_api(router: APIRouter, path: str, mapper: CRUDEntitySchemaMapper,
                        get_crud_service: Optional[Callable] = None):
    pk_column = mapper.pk_column
    s_props = mapper.update_schema_entity_tuples

    @router.patch(path, response_model=APIResult[mapper.update_schema])
    def update(service: CRUDService[Entity] = Depends(get_crud_service),
               pk: pk_column.type.python_type = Path(..., alias=pk_column.name),
               data: mapper.update_schema = Body(...)):
        result = service.update(pk, data.dict(exclude_unset=True))
        return APIResult(
            data=mapper.update_schema(**{s_k: getattr(result, e_k) for s_k, e_k in s_props if hasattr(result, e_k)}))


def register_delete_api(router: APIRouter, path: str, mapper: CRUDEntitySchemaMapper,
                        get_crud_service: Optional[Callable] = None):
    pk_column = mapper.pk_column

    @router.delete(path, response_model=APIResult[Literal['OK']])
    def delete(service: CRUDService[Entity] = Depends(get_crud_service),
               pk: pk_column.type.python_type = Path(..., alias=pk_column.name)):
        print('delete', pk)
        service.delete_or_fail(pk)
        return APIResult(data='OK')
