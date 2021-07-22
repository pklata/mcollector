from sqlalchemy import JSON, Column, Integer, String, Table

from mcollector.db import DBManager
from mcollector.locations.models import Building

buildings = Table(
    "buildings",
    DBManager.mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("country", String),
    Column("address", String),
    Column("zip_code", String),
    Column("city", String),
    Column("county", String),
    Column("locals", JSON),
)

DBManager.add_mapping(Building, buildings)
