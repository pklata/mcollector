from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from pydantic.main import BaseModel

from mcollector.errors import NotFoundError
from mcollector.fastapi import app
from mcollector.locations import service
from mcollector.locations.uow import uow_factory


class BuildingPresentation(BaseModel):
    id: Optional[int] = None
    country: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None


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


class LocalPresentation(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None
    description: Optional[str] = None


class LocalUpdate(BaseModel):
    number: Optional[int] = None
    description: Optional[str] = None


class LocalCreate(BaseModel):
    number: int
    description: Optional[str] = None


class IdResponse(BaseModel):
    id: int


@app.get("/building", response_model=List[BuildingPresentation])
async def list_buildings() -> List[Dict[str, Any]]:
    return await service.list_buildings(uow_factory())


@app.get("/building/{building_id}", response_model=BuildingPresentation)
async def get_building(building_id: int) -> Dict[str, Any]:
    try:
        return await service.get_building(building_id, uow_factory())
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.post("/building", response_model=IdResponse)
async def add_building(new_building: BuildingCreate) -> Dict[str, int]:
    try:
        return await service.add_building(
            new_building.dict(exclude_unset=True), uow_factory()
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.patch("/building/{building_id}", response_model=IdResponse)
async def update_building(
    building_update: BuildingUpdate, building_id: int
) -> Dict[str, int]:
    try:
        return await service.update_building(
            building_id, building_update.dict(exclude_unset=True), uow_factory()
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.delete("/building/{building_id}")
async def delete_building(building_id: int) -> Dict[str, int]:
    try:
        return await service.delete_building(building_id, uow_factory())
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.get("/building/{building_id}/local", response_model=List[LocalPresentation])
async def list_locals(building_id: int) -> List[Dict[str, Any]]:
    return await service.list_locals(building_id, uow_factory())


@app.get("/local/{local_id}", response_model=LocalPresentation)
async def get_local(local_id: int) -> Dict[str, Any]:
    try:
        return await service.get_local(local_id, uow_factory())
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.post("/building/{building_id}/local", response_model=IdResponse)
async def add_local(new_local: LocalCreate, building_id: int) -> Dict[str, int]:
    try:
        return await service.add_local(
            building_id, new_local.dict(exclude_unset=True), uow_factory()
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.patch("/local/{local_id}", response_model=IdResponse)
async def update_local(local_update: LocalUpdate, local_id: int) -> Dict[str, int]:
    try:
        return await service.update_local(
            local_id, local_update.dict(exclude_unset=True), uow_factory()
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.delete("/local/{local_id}")
async def delete_local(local_id: int) -> Dict[str, int]:
    try:
        return await service.delete_local(local_id, uow_factory())
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
