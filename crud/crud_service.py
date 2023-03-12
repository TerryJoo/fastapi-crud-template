import abc
from typing import Generic, Optional, List, Iterable

from fastapi import Depends
from sqlalchemy import update, delete, select, insert, func, Column, Operators
from sqlalchemy.orm import Session

from crud.types import Entity
from dbs.sqlite3 import get_session


class CRUDService(Generic[Entity]):
    @property
    @abc.abstractmethod
    def entity(self) -> Entity.__class__:
        pass

    @property
    def entity_pk(self) -> Column:
        return self.entity.__table__.primary_key.columns.values()[0]

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def find_by_id(self, id) -> Optional[Entity]:
        return self.session.get(self.entity, id)

    def count(self, where=None) -> int:
        qb = select(func.count(self.entity_pk))
        if where:
            qb = qb.where(where)
        return self.session.execute(qb).scalar()

    def find_many(self, limit: int = 0, offset: int = 10, where: Optional[Iterable[Operators]] = None,
                  order_by: Optional[Iterable[Operators]] = None):
        qb = select(self.entity).limit(limit).offset(offset)
        if where:
            qb = qb.where(*where)
        if order_by:
            qb = qb.order_by(*order_by)
        return self.session.execute(qb).scalars().all()

    def create(self, data: dict) -> Entity:
        return self.session.execute(insert(self.entity).returning(self.entity), data).scalar()

    def create_bulk(self, data: List[dict]):
        return self.session.execute(insert(self.entity).returning(self.entity), data).scalars().all()

    def update(self, id, data: dict) -> Entity:
        return self.session.execute(update(self.entity)
                                    .where(self.entity_pk == id)
                                    .values(**data)
                                    .returning(self.entity)).scalar()

    def delete(self, id):
        return self.session.execute(delete(self.entity).where(self.entity_pk == id)).one_or_none()

    def delete_or_fail(self, id):
        return self.session.execute(delete(self.entity).where(self.entity_pk == id)).one()
