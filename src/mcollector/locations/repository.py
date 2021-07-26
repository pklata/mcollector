from typing import Any, Dict, List

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.exc import UnmappedInstanceError

from mcollector.errors import NotFoundError
from mcollector.locations.models import Building, Local


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
        return _id

    async def list_locals(self, building_id: int) -> List[Local]:
        results = await self.session.execute(
            select(Local).where(Local.building_id == building_id).order_by(Local.number)
        )
        return results.scalars().all()

    async def get_local(self, local_id: int) -> Local:
        local = await self.session.get(Local, local_id)
        if not local:
            raise NotFoundError(Local.__name__, local_id)
        return local

    async def add_local(self, building_id: int, params: Dict[str, Any]) -> int:
        local = Local(**params)
        local.building_id = building_id
        self.session.add(local)
        await self.session.flush()
        assert local.id
        return local.id

    async def delete_local(self, _id: int) -> None:
        local = await self.session.get(Local, _id)
        try:
            await self.session.delete(local)
        except UnmappedInstanceError:
            raise NotFoundError(Local.__name__, _id)

    async def update_local(self, _id: int, **kwargs: Dict[str, Any]) -> int:
        result = await self.session.execute(
            update(Local).where(Local.id == _id).values(**kwargs)
        )
        if not result.rowcount:
            raise NotFoundError(Local.__name__, _id)
        await self.session.flush()
        return _id
