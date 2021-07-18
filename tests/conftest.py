import asyncio
from typing import Callable

import pytest
from mcollector_tests.factories import BuildingFactory, async_factory  # noqa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from mcollector.db.mappings import SessionManager, mapper_registry, start_mappers
from mcollector.domain.models import CircuitMeasurementData, Local


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine("sqlite+aiosqlite://", future=True)
    start_mappers()
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)
    return engine


@pytest.fixture
async def session(async_engine, monkeypatch):
    async with AsyncSession(
        async_engine, future=True, expire_on_commit=False
    ) as session:

        def get_session(x):
            return session

        monkeypatch.setattr(SessionManager, "get_session", get_session)
        # TODO try without monkeypatch
        nested = await session.begin_nested()
        yield session
        await nested.rollback()


@pytest.fixture
async def building(session) -> Callable:
    return await async_factory(BuildingFactory, session)


@pytest.fixture
def local():
    return Local(7)


@pytest.fixture
def c_meas_data():
    return CircuitMeasurementData(
        device="B-16", i_n=16.0, u_n=230.0, i_off=80.0, z_m=0.44, z_s=2.88
    )
