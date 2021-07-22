from typing import Any, Dict, List

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.exc import UnmappedInstanceError

from mcollector.base_model import BaseModel
from mcollector.errors import NotFoundError


class GenericRepository:
    model: BaseModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> List[BaseModel]:
        results = await self.session.execute(select(self.model))
        return results.scalars().all()

    async def get(self, _id: int) -> BaseModel:
        obj = await self.session.get(self.model, _id)
        if not obj:
            raise NotFoundError(self.model.__name__, _id)
        return obj

    async def add(self, params: Dict[str, Any]) -> int:
        obj = self.model(**params)
        self.session.add(obj)
        await self.session.flush()
        assert obj.id
        return obj.id

    async def delete(self, _id: int) -> None:
        obj = await self.session.get(self.model, _id)
        try:
            await self.session.delete(obj)
        except UnmappedInstanceError:
            raise NotFoundError(self.model.__name__, _id)

    async def update(self, _id: int, **kwargs: Dict[str, Any]) -> int:
        result = await self.session.execute(
            update(self.model).where(self.model.id == _id).values(**kwargs)
        )
        if not result.rowcount:
            raise NotFoundError(self.model.__name__, _id)
        await self.session.flush()
        return result.lastrowid
