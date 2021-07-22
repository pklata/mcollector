from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseModel:
    id: Optional[int] = None
