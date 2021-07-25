from typing import Any, Dict, List

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.exc import UnmappedInstanceError

from mcollector.errors import NotFoundError
from mcollector.locations.models import Building


class BuildingsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> List[Building]:
        results = await self.session.execute(select(Building))
        return results.scalars().all()

    async def get(self, _id: int) -> Building:
        building = await self.session.get(Building, _id)
        if not building:
            raise NotFoundError(Building.__name__, _id)
        return building

    async def add(self, params: Dict[str, Any]) -> int:
        building = Building(**params)
        self.session.add(building)
        await self.session.flush()
        assert building.id
        return building.id

    async def delete(self, _id: int) -> None:
        building = await self.session.get(Building, _id)
        try:
            await self.session.delete(building)
        except UnmappedInstanceError:
            raise NotFoundError(Building.__name__, _id)

    async def update(self, _id: int, **kwargs: Dict[str, Any]) -> int:
        result = await self.session.execute(
            update(Building).where(Building.id == _id).values(**kwargs)
        )
        if not result.rowcount:
            raise NotFoundError(Building.__name__, _id)
        await self.session.flush()
        return result.lastrowid
