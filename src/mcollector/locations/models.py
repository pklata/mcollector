from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Local:
    """Local where the part of inspection is taking place. Part of the building"""

    number: int


@dataclass
class Building:
    """Building where inspection is taking place"""

    id: Optional[int] = None
    country: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    locals: List[Local] = field(default_factory=list)

    def get_locals(self) -> List[Local]:
        return sorted(self.locals, key=lambda l: l.number)

    def add(self, local: Local) -> None:
        self.locals.append(local)

    def filter_locals(self, match: str) -> List[Local]:
        _locals = [local for local in self.locals if match in str(local.number)]
        return sorted(_locals, key=lambda l: l.number)
