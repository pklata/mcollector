from typing import List, Optional

from pydantic.fields import Field
from pydantic.main import BaseModel

from mcollector.db.mappings import SessionManager
from mcollector.domain.models import Building, Local
from mcollector.entrypoints.fastapi.app import app
from mcollector.repository.buildings_repository import BuildingsRepository


class BuildingPresentation(BaseModel):
    # TODO maybe something simpler?
    id: Optional[int] = None
    country: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    locals: List[Local] = Field(default_factory=list)


def serialize(buildings: List[Building]) -> List[BuildingPresentation]:
    return [
        BuildingPresentation(
            id=building.id,
            country=building.country,
            address=building.address,
            zip_code=building.zip_code,
            city=building.city,
            county=building.county,
            locals=building.locals,
        )
        for building in buildings
    ]


@app.get("/building", response_model=List[BuildingPresentation])
async def get_buildings() -> List[BuildingPresentation]:
    buildings = await BuildingsRepository(SessionManager().get_session()).list()
    return serialize(buildings)
