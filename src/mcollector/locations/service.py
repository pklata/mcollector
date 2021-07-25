from dataclasses import asdict
from typing import Any, Dict, List

from mcollector.locations.uow import LocationsUnitOfWork


async def list(uow: LocationsUnitOfWork) -> List[Dict[str, Any]]:
    async with uow:
        buildings = await uow.buildings.list()
    return [asdict(b) for b in buildings]


async def get(building_id: int, uow: LocationsUnitOfWork) -> Dict[str, Any]:
    async with uow:
        building = await uow.buildings.get(building_id)
    return asdict(building)


async def add(
    building_params: Dict[str, Any], uow: LocationsUnitOfWork
) -> Dict[str, int]:
    async with uow:
        _id = await uow.buildings.add(building_params)
        await uow.commit()
    return {"id": _id}


async def update(
    building_id: int, building_params: Dict[str, Any], uow: LocationsUnitOfWork
) -> Dict[str, int]:
    async with uow:
        _id = await uow.buildings.update(building_id, **building_params)
        await uow.commit()
    return {"id": _id}


async def delete(building_id: int, uow: LocationsUnitOfWork) -> Dict[str, int]:
    async with uow:
        await uow.buildings.delete(building_id)
        await uow.commit()
    return {}
