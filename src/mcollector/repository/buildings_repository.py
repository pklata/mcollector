from typing import Any, Dict, List

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.exc import UnmappedInstanceError

from mcollector.domain.models import Building


class BuildingNotFound(Exception):
    pass


class BuildingsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> List[Building]:
        results = await self.session.execute(select(Building))
        return results.scalars().all()

    async def get(self, building_id: int) -> Building:
        building = await self.session.get(Building, building_id)
        if not building:
            raise BuildingNotFound(f"Building with id:{building_id} not found.")
        return building

    def add(self, building: Building) -> None:
        self.session.add(building)

    async def delete(self, building_id: int) -> None:
        building = await self.session.get(Building, building_id)
        try:
            await self.session.delete(building)
        except UnmappedInstanceError:
            raise BuildingNotFound(f"Building with id:{building_id} not found.")

    async def update(self, building_id: int, **kwargs: Dict[str, Any]) -> Building:
        result = await self.session.execute(
            update(Building).where(Building.id == building_id).values(**kwargs)
        )
        if not result.rowcount:
            raise BuildingNotFound(f"Building with id:{building_id} not found.")
        await self.session.flush()
        return result.lastrowid
