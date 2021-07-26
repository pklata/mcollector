from dataclasses import dataclass
from typing import Optional

from mcollector.base_model import BaseModel


@dataclass
class Local(BaseModel):
    """Local where the part of inspection is taking place. Part of the building"""

    id: Optional[int] = None
    number: Optional[int] = None
    description: Optional[str] = None
    building_id: Optional[int] = None


@dataclass
class Building(BaseModel):
    """Building where inspection is taking place"""

    id: Optional[int] = None
    country: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
