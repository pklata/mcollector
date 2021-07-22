from typing import Any, Dict, List

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.exc import UnmappedInstanceError

from mcollector.errors import NotFoundError
from mcollector.locations.models import Building


class BuildingNotFoundError(NotFoundError):
    def __init__(self, building_id: int):
        super().__init__(f"Building with id: {building_id} not found.")


class BuildingsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> List[Building]:
        results = await self.session.execute(select(Building))
        return results.scalars().all()

    async def get(self, building_id: int) -> Building:
        building = await self.session.get(Building, building_id)
        if not building:
            raise BuildingNotFoundError(building_id)
        return building

    async def add(self, building_params: Dict[str, Any]) -> int:
        building = Building(**building_params)
        self.session.add(building)
        await self.session.flush()
        assert building.id
        return building.id

    async def delete(self, building_id: int) -> None:
        building = await self.session.get(Building, building_id)
        try:
            await self.session.delete(building)
        except UnmappedInstanceError:
            raise BuildingNotFoundError(building_id)

    async def update(self, building_id: int, **kwargs: Dict[str, Any]) -> int:
        result = await self.session.execute(
            update(Building).where(Building.id == building_id).values(**kwargs)
        )
        if not result.rowcount:
            raise BuildingNotFoundError(building_id)
        await self.session.flush()
        return result.lastrowid
