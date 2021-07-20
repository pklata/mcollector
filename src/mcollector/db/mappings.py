from sqlalchemy import JSON, Column, Integer, String, Table
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
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


class DBManager:
    mapping_started = False
    engine = None
    session = None

    @classmethod
    def start_mappers(cls) -> None:
        if cls.mapping_started:
            return
        mapper_registry.map_imperatively(Building, buildings)

        cls.mapping_started = True

    @classmethod
    async def recreate_db(cls) -> None:
        async with cls.get_engine().begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        if not cls.engine:
            cls.engine = create_async_engine("sqlite+aiosqlite://", future=True)
        return cls.engine

    @classmethod
    def get_session(cls) -> AsyncSession:
        if not cls.session:
            cls.session = AsyncSession(cls.engine, future=True, expire_on_commit=False)
        return cls.session
