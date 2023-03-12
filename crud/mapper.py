from typing import Optional, List, Tuple

from pydantic import BaseModel
from sqlalchemy import Column

from crud.types import Entity


class CRUDEntitySchemaMapper:
    @property
    def pk_column(self) -> Column:
        return self.entity.__table__.primary_key.columns.values()[0]

    def __init__(self, entity: Entity,
                 read_schema: Optional[BaseModel.__class__] = None,
                 list_schema: Optional[BaseModel.__class__] = None,
                 create_schema: Optional[BaseModel.__class__] = None,
                 update_schema: Optional[BaseModel.__class__] = None,
                 delete_api: bool = True,
                 schema_entity_keys_mapping: Optional[List[Tuple[str, str]]] = None):
        self.entity = entity
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.read_schema = read_schema
        self.list_schema = list_schema
        self.delete_api = delete_api
        self.schema_entity_keys_mapping = schema_entity_keys_mapping or [(k, k) for k in
                                                                         self.entity.__table__.columns.keys()]
        self.entity_key_by_schema_key = {s_key: e_key for s_key, e_key in self.schema_entity_keys_mapping}
        self.schema_key_by_entity_key = {e_key: s_key for s_key, e_key in self.schema_entity_keys_mapping}

    @property
    def list_schema_entity_tuples(self) -> List[Tuple[str, str]]:
        result = []
        for prop in self.list_schema.__fields__:
            result.append((prop, self.entity_key_by_schema_key[prop]))
        return result

    @property
    def read_schema_entity_tuples(self) -> List[Tuple[str, str]]:
        result = []
        for prop in self.read_schema.__fields__:
            result.append((prop, self.entity_key_by_schema_key[prop]))
        return result

    @property
    def create_schema_entity_tuples(self) -> List[Tuple[str, str]]:
        result = []
        for prop in self.create_schema.__fields__:
            result.append((prop, self.entity_key_by_schema_key[prop]))
        return result

    @property
    def update_schema_entity_tuples(self) -> List[Tuple[str, str]]:
        result = []
        for prop in self.update_schema.__fields__:
            result.append((prop, self.entity_key_by_schema_key[prop]))
        return result
