from dataclasses import asdict
from typing import Any, Dict, List

from mcollector.locations.uow import LocationsUnitOfWork


async def list_buildings(uow: LocationsUnitOfWork) -> List[Dict[str, Any]]:
    async with uow:
        buildings = await uow.locations.list_buildings()
    return [asdict(b) for b in buildings]


async def get_building(building_id: int, uow: LocationsUnitOfWork) -> Dict[str, Any]:
    async with uow:
        building = await uow.locations.get_building(building_id)
    return asdict(building)


async def add_building(
    building_params: Dict[str, Any], uow: LocationsUnitOfWork
) -> Dict[str, int]:
    async with uow:
        _id = await uow.locations.add_building(building_params)
        await uow.commit()
    return {"id": _id}


async def update_building(
    building_id: int, building_params: Dict[str, Any], uow: LocationsUnitOfWork
) -> Dict[str, int]:
    async with uow:
        _id = await uow.locations.update_building(building_id, **building_params)
        await uow.commit()
    return {"id": _id}


async def delete_building(building_id: int, uow: LocationsUnitOfWork) -> Dict[str, int]:
    async with uow:
        await uow.locations.delete_building(building_id)
        await uow.commit()
    return {}


async def list_locals(
    building_id: int, uow: LocationsUnitOfWork
) -> List[Dict[str, Any]]:
    async with uow:
        locals_ = await uow.locations.list_locals(building_id)
    return [asdict(b) for b in locals_]


async def get_local(local_id: int, uow: LocationsUnitOfWork) -> Dict[str, Any]:
    async with uow:
        local = await uow.locations.get_local(local_id)
    return asdict(local)


async def add_local(
    building_id: int, local_params: Dict[str, Any], uow: LocationsUnitOfWork
) -> Dict[str, int]:
    async with uow:
        _id = await uow.locations.add_local(building_id, local_params)
        await uow.commit()
    return {"id": _id}


async def update_local(
    local_id: int, local_params: Dict[str, Any], uow: LocationsUnitOfWork
) -> Dict[str, int]:
    async with uow:
        _id = await uow.locations.update_local(local_id, **local_params)
        await uow.commit()
    return {"id": _id}


async def delete_local(local_id: int, uow: LocationsUnitOfWork) -> Dict[str, int]:
    async with uow:
        await uow.locations.delete_local(local_id)
        await uow.commit()
    return {}
