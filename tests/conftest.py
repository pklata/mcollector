import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from mcollector.db.mappings import mapper_registry, start_mappers
from mcollector.domain.models import Building, CircuitMeasurementData, Local


@pytest.fixture(scope="session")
def async_engine():
    engine = create_async_engine("sqlite+aiosqlite://", future=True)
    start_mappers()
    return engine


@pytest.fixture
async def session(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)

    async with AsyncSession(async_engine, future=True) as session:
        yield session


@pytest.fixture
def building():
    return Building(
        country="Polska",
        address="Towarowa 365",
        zip_code="02-200",
        city="Warszawa",
        county="mazowieckie",
    )


@pytest.fixture
def local():
    return Local(7)


@pytest.fixture
def c_meas_data():
    return CircuitMeasurementData(
        device="B-16", i_n=16.0, u_n=230.0, i_off=80.0, z_m=0.44, z_s=2.88
    )
