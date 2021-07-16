from sqlalchemy import JSON, Column, Integer, String, Table
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
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


async_engine = create_async_engine("sqlite+aiosqlite://", future=True)


class SessionManager:
    def get_session(self) -> AsyncSession:
        return AsyncSession(async_engine, future=True, expire_on_commit=False)
