from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory

from mcollector.db import DBManager
from mcollector.locations.repository import BuildingsRepository
from mcollector.locations.uow import LocationsUnitOfWork


@pytest.mark.asyncio
@pytest.mark.usefixtures("recreate_db")
class TestUnitOfWork:
    async def test_uow_can_list_all_batches(self):
        building1 = BuildingFactory()
        building1.id = await BuildingsRepository(DBManager.session_factory()).add(
            asdict(building1)
        )
        async with LocationsUnitOfWork(DBManager.session_factory) as uow:
            buildings = await uow.buildings.list()
            assert buildings == [building1]

    async def test_explicit_commit_works(self):
        async with LocationsUnitOfWork(DBManager.session_factory) as uow:
            building1 = BuildingFactory()
            building1.id = await uow.buildings.add(asdict(building1))
            await uow.commit()

        buildings = await BuildingsRepository(DBManager.session_factory()).list()
        assert buildings == [building1]

    async def test_rollback_works(self):
        class TestException(Exception):
            pass

        with pytest.raises(TestException):
            async with LocationsUnitOfWork(DBManager.session_factory) as uow:
                building1 = BuildingFactory()
                building1.id = await uow.buildings.add(asdict(building1))
                raise TestException()

        buildings = await BuildingsRepository(DBManager.session_factory()).list()
        assert buildings == []
