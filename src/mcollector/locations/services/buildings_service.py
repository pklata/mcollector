from dataclasses import asdict
from typing import Any, Dict, List

from mcollector.locations.db.mappings import DBManager
from mcollector.locations.repository.buildings_repository import BuildingsRepository


async def list() -> List[Dict[str, Any]]:
    buildings = await BuildingsRepository(DBManager.get_session()).list()
    return [asdict(b) for b in buildings]


async def get(building_id: int) -> Dict[str, Any]:
    building = await BuildingsRepository(DBManager.get_session()).get(building_id)
    return asdict(building)


async def add(building_params: Dict[str, Any]) -> Dict[str, int]:
    session = DBManager.get_session()
    _id = await BuildingsRepository(session).add(building_params)
    return {"id": _id}


async def update(building_id: int, building_params: Dict[str, Any]) -> Dict[str, int]:
    session = DBManager.get_session()
    _id = await BuildingsRepository(session).update(building_id, **building_params)
    return {"id": _id}


async def delete(building_id: int) -> Dict[str, int]:
    session = DBManager.get_session()
    await BuildingsRepository(session).delete(building_id)
    return {}
