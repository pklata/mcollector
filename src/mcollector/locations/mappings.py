from sqlalchemy import Column, ForeignKey, Integer, String, Table

from mcollector.db import DBManager
from mcollector.locations.models import Building, Local

buildings = Table(
    "buildings",
    DBManager.mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("country", String),
    Column("address", String),
    Column("zip_code", String),
    Column("city", String),
    Column("county", String),
)

locals = Table(
    "locals",
    DBManager.mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("number", Integer),
    Column("description", String),
    Column("building_id", Integer, ForeignKey("buildings.id")),
)

DBManager.add_mapping(Building, buildings)
DBManager.add_mapping(Local, locals)
