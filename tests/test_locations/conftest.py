import pytest

from mcollector.db import DBManager
from mcollector.locations.uow import LocationsUnitOfWork


@pytest.fixture
async def locals_setup(session, building, local):
    building_ = building(id=1)
    session.add(building_)
    local1 = local(number=7, building_id=building_.id)
    local2 = local(number=2, building_id=building_.id)
    session.add(local1)
    session.add(local2)
    await session.commit()
    return [local2, local1]


@pytest.fixture
def uow():
    return LocationsUnitOfWork(DBManager.session_factory)
