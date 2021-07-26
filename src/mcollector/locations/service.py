from dataclasses import asdict
from typing import Any, Dict, List

from mcollector.locations.uow import LocationsUnitOfWork


async def list_buildings(uow: LocationsUnitOfWork) -> List[Dict[str, Any]]:
    async with uow:
        buildings = await uow.buildings.list_buildings()
    return [asdict(b) for b in buildings]


async def get_building(building_id: int, uow: LocationsUnitOfWork) -> Dict[str, Any]:
    async with uow:
        building = await uow.buildings.get_building(building_id)
    return asdict(building)


async def add_building(
    building_params: Dict[str, Any], uow: LocationsUnitOfWork
) -> Dict[str, int]:
    async with uow:
        _id = await uow.buildings.add_building(building_params)
        await uow.commit()
    return {"id": _id}


async def update_building(
    building_id: int, building_params: Dict[str, Any], uow: LocationsUnitOfWork
) -> Dict[str, int]:
    async with uow:
        _id = await uow.buildings.update_building(building_id, **building_params)
        await uow.commit()
    return {"id": _id}


async def delete_building(building_id: int, uow: LocationsUnitOfWork) -> Dict[str, int]:
    async with uow:
        await uow.buildings.delete_building(building_id)
        await uow.commit()
    return {}
