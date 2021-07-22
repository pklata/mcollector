import asyncio
from typing import Callable

import pytest
from mcollector_tests.factories import BuildingFactory, async_factory

from mcollector.locations.mappings import DBManager
from mcollector.locations.models import CircuitMeasurementData, Local


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    DBManager.start_mappers()
    await DBManager.recreate_db()
    return DBManager.get_engine()


@pytest.fixture
async def session(async_engine):
    async with DBManager.get_session() as session:
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
