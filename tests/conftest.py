import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from mcollector.domain.models import Building, CircuitMeasurementData, Local
from mcollector.orm.mappings import mapper_registry, start_mappers


@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite://", future=True)
    start_mappers()
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)

    async with AsyncSession(engine, future=True) as session:
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
