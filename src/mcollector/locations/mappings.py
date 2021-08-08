from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

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
    Column("building_id", Integer, ForeignKey("buildings.id"), nullable=False),
)

DBManager.add_mapping(
    Building,
    buildings,
    properties={
        "locals": relationship(Local, lazy="noload", back_populates="building")
    },
)
DBManager.add_mapping(
    Local,
    locals,
    properties={
        "building": relationship(Building, lazy="noload", back_populates="locals")
    },
)
