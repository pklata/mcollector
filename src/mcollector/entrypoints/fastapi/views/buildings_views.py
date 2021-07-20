from dataclasses import asdict
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from pydantic.fields import Field
from pydantic.main import BaseModel

from mcollector.db.mappings import DBManager
from mcollector.domain.models import Building, Local
from mcollector.entrypoints.fastapi.app import app
from mcollector.repository.buildings_repository import (
    BuildingNotFoundError,
    BuildingsRepository,
)


class BuildingPresentation(BaseModel):
    id: Optional[int] = None
    country: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    locals: List[Local] = Field(default_factory=list)


class BuildingUpdate(BaseModel):
    country: Optional[str]
    address: Optional[str]
    zip_code: Optional[str]
    city: Optional[str]
    county: Optional[str]


class BuildingCreate(BaseModel):
    country: Optional[str]
    address: str
    zip_code: Optional[str]
    city: Optional[str]
    county: Optional[str]


class BuildingIdResponse(BaseModel):
    id: int


@app.get("/building", response_model=List[BuildingPresentation])
async def get_building() -> List[Dict[str, Any]]:
    buildings = await BuildingsRepository(DBManager.get_session()).list()
    return [asdict(b) for b in buildings]


@app.get("/building/{building_id}", response_model=BuildingPresentation)
async def list_buildings(building_id: int) -> Dict[str, Any]:
    try:
        building = await BuildingsRepository(DBManager.get_session()).get(building_id)
    except BuildingNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    return asdict(building)


@app.post("/building", response_model=BuildingIdResponse)
async def add_building(new_building: BuildingCreate) -> BuildingIdResponse:
    try:
        session = DBManager.get_session()
        _id = await BuildingsRepository(session).add(
            Building(**new_building.dict(exclude_unset=True))
        )
    except BuildingNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    return BuildingIdResponse(id=_id)


@app.patch("/building/{building_id}", response_model=BuildingIdResponse)
async def update_building(
    building_update: BuildingUpdate, building_id: int
) -> BuildingIdResponse:
    try:
        session = DBManager.get_session()
        _id = await BuildingsRepository(session).update(
            building_id, **building_update.dict(exclude_unset=True)
        )
    except BuildingNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    return BuildingIdResponse(id=_id)


@app.delete("/building/{building_id}")
async def delete_building(building_id: int) -> Dict[str, int]:
    try:
        session = DBManager.get_session()
        await BuildingsRepository(session).delete(building_id)
    except BuildingNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    return {}
