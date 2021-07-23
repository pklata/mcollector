from typing import Any, Set, Tuple

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import registry


class DBManager:
    mapper_registry = registry()
    mapping_started = False
    engine = None
    session = None
    mappings: Set[Tuple[Any, Any]] = set()

    @classmethod
    def add_mapping(cls, model: Any, mapping: Any) -> None:
        cls.mappings.add((model, mapping))

    @classmethod
    def start_mappers(cls) -> None:
        if cls.mapping_started:
            return
        for mapping in cls.mappings:
            cls.mapper_registry.map_imperatively(*mapping)

        cls.mapping_started = True

    @classmethod
    async def recreate_db(cls) -> None:
        async with cls.get_engine().begin() as conn:
            await conn.run_sync(cls.mapper_registry.metadata.drop_all)
            await conn.run_sync(cls.mapper_registry.metadata.create_all)

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        if not cls.engine:
            cls.engine = create_async_engine("sqlite+aiosqlite://", future=True)
        return cls.engine

    @classmethod
    def session_factory(cls) -> AsyncSession:
        return AsyncSession(cls.engine, future=True, expire_on_commit=False)
