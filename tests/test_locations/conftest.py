import pytest

from mcollector.db import DBManager
from mcollector.locations.uow import LocationsUnitOfWork


@pytest.fixture
async def locals_setup(session, building, local):
    building_ = building(id=1)
    session.add_building(building_)
    local1 = local(number=7, building_id=building_.id)
    local2 = local(number=2, building_id=building_.id)
    session.add_building(local1)
    session.add_building(local2)
    await session.commit()
    return [local2, local1]


@pytest.fixture
def uow():
    return LocationsUnitOfWork(DBManager.session_factory)
