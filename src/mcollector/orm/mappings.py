from sqlalchemy import JSON, Column, Integer, String, Table
from sqlalchemy.orm import registry

from mcollector.domain.models import Building

mapper_registry = registry()

buildings = Table(
    "buildings",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("country", String),
    Column("address", String),
    Column("zip_code", String),
    Column("city", String),
    Column("county", String),
    Column("locals", JSON),
)


def start_mappers() -> None:
    mapper_registry.map_imperatively(Building, buildings)
