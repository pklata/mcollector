from dataclasses import asdict
from typing import Any, Dict, List, Optional

from pydantic.fields import Field
from pydantic.main import BaseModel

from mcollector.db.mappings import DBManager
from mcollector.domain.models import Local
from mcollector.entrypoints.fastapi.app import app
from mcollector.repository.buildings_repository import BuildingsRepository


class BuildingPresentation(BaseModel):
    id: Optional[int] = None
    country: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    locals: List[Local] = Field(default_factory=list)


def dataclasses_to_dict(d_classes: List[Any]) -> List[Dict[str, Any]]:
    return [asdict(d_class) for d_class in d_classes]


@app.get("/building", response_model=List[BuildingPresentation])
async def get_buildings() -> List[Dict[str, Any]]:
    buildings = await BuildingsRepository(DBManager.get_session()).list()
    return dataclasses_to_dict(buildings)
