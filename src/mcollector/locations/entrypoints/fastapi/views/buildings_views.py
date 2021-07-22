from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from pydantic.fields import Field
from pydantic.main import BaseModel

from mcollector.locations.domain.models import Local
from mcollector.locations.entrypoints.fastapi.app import app
from mcollector.locations.repository.buildings_repository import BuildingNotFoundError
from mcollector.locations.services import buildings_service


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
async def list_buildings() -> List[Dict[str, Any]]:
    return await buildings_service.list()


@app.get("/building/{building_id}", response_model=BuildingPresentation)
async def get_building(building_id: int) -> Dict[str, Any]:
    try:
        return await buildings_service.get(building_id)
    except BuildingNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.post("/building", response_model=BuildingIdResponse)
async def add_building(new_building: BuildingCreate) -> Dict[str, int]:
    try:
        return await buildings_service.add(new_building.dict(exclude_unset=True))
    except BuildingNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.patch("/building/{building_id}", response_model=BuildingIdResponse)
async def update_building(
    building_update: BuildingUpdate, building_id: int
) -> Dict[str, int]:
    try:
        return await buildings_service.update(
            building_id, building_update.dict(exclude_unset=True)
        )
    except BuildingNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.delete("/building/{building_id}")
async def delete_building(building_id: int) -> Dict[str, int]:
    try:
        return await buildings_service.delete(building_id)
    except BuildingNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)