from typing import Generic, List, Optional, Callable, Iterable, Tuple

from fastapi.params import Query
from pydantic import BaseModel
from pydantic.generics import GenericModel
from sqlalchemy import Operators

from crud.mapper import CRUDEntitySchemaMapper
from crud.types import Schema, T


def create_sort_dto(schema_entity_tuples: List[Tuple[str, str]], mapper: CRUDEntitySchemaMapper) -> Callable:
    def sort_dto(sort: Optional[str] = Query(
        default=None,
        alias="$sorts",
        example=','.join(map(lambda f: f'-{f[0]}', schema_entity_tuples))),
    ) -> Iterable[Operators]:
        result = []
        for f in sort.split(','):
            f, order = (f[1:], 'desc') if f.startswith('-') else (f, 'asc')
            if f not in mapper.entity_key_by_schema_key:
                raise ValueError(f"Invalid sort field: {f}")
            column = getattr(mapper.entity, mapper.entity_key_by_schema_key[f])
            result.append(getattr(column, order)())
        return result

    return sort_dto


class PaginationDto(BaseModel):
    page: int = 0
    per_page: int = 10

    @property
    def offset(self):
        return self.per_page * (self.page - 1)

    @property
    def limit(self):
        return self.per_page

    def to_query_dict(self):
        return {"offset": self.offset, "limit": self.limit}


class APIResult(GenericModel, Generic[Schema]):
    data: Schema


class ListResult(GenericModel, Generic[Schema]):
    data: List[Schema]


class PaginatedResult(ListResult[Schema], Generic[Schema]):
    total_count: int
    data: List[Schema]


class DeletedResult(GenericModel, Generic[T]):
    id: T
