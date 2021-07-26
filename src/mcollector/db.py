from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import registry


@dataclass
class Mapping:
    model: Any
    mapping: Any
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]


class DBManager:
    mapper_registry = registry()
    mapping_started = False
    engine = None
    session = None
    mappings: List[Mapping] = []

    @classmethod
    def add_mapping(
        cls, model: Any, mapping: Any, *args: Any, **kwargs: Dict[str, Any]
    ) -> None:
        cls.mappings.append(
            Mapping(model=model, mapping=mapping, args=args, kwargs=kwargs)
        )

    @classmethod
    def start_mappers(cls) -> None:
        if cls.mapping_started:
            return
        for mapping in cls.mappings:
            cls.mapper_registry.map_imperatively(
                mapping.model, mapping.mapping, *mapping.args, **mapping.kwargs
            )

        cls.mapping_started = True

    @classmethod
    async def recreate_db(cls) -> None:
        async with cls.get_engine().begin() as conn:
            await conn.run_sync(cls.mapper_registry.metadata.drop_all)
            await conn.run_sync(cls.mapper_registry.metadata.create_all)

    @classmethod
    async def create_db(cls) -> None:
        async with cls.get_engine().begin() as conn:
            await conn.run_sync(cls.mapper_registry.metadata.create_all)

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        if not cls.engine:
            cls.engine = create_async_engine("sqlite+aiosqlite://", future=True)
        return cls.engine

    @classmethod
    def session_factory(cls) -> AsyncSession:
        return AsyncSession(cls.engine, future=True, expire_on_commit=False)
