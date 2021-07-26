from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory

from mcollector.errors import NotFoundError
from mcollector.locations import service
from mcollector.locations.models import Building


@pytest.mark.asyncio
@pytest.mark.usefixtures("recreate_db")
class TestLocationsService:
    async def test_list(self, building, session, uow):
        building1 = building()
        building2 = building()
        session.add(building1)
        session.add(building2)
        await session.commit()
        buildings = await service.list_buildings(uow)
        assert buildings == [asdict(building1), asdict(building2)]

    async def test_get(self, building, session, uow):
        building1 = building(id=1)
        session.add(building1)
        await session.commit()
        building_ = await service.get_building(1, uow)
        assert building_ == asdict(building1)

    async def test_get_non_existing(self, uow):
        with pytest.raises(NotFoundError):
            await service.get_building(1, uow)

    async def test_add(self, uow):
        building1 = BuildingFactory()
        result = await service.add_building(asdict(building1), uow)
        buildings = await service.list_buildings(uow)
        building1.id = result["id"]
        assert result == {"id": 1}
        assert buildings == [asdict(building1)]

    async def test_delete(self, building, session, uow):
        session.add(building(id=1))
        await session.commit()
        await service.delete_building(1, uow)
        buildings = await service.list_buildings(uow)
        assert buildings == []

    async def test_delete_non_existing(self, uow):
        with pytest.raises(NotFoundError):
            await service.delete_building(1, uow)

    async def test_update(self, session, building, uow):
        session.add(building())
        await session.commit()
        result = await service.update_building(
            1, {"country": "Anglia", "address": "Graniczna 11"}, uow
        )
        assert result == {"id": 1}
        assert await session.get(Building, 1) == Building(
            address="Graniczna 11",
            city="Warszawa",
            country="Anglia",
            county="mazowieckie",
            id=1,
            zip_code="02-200",
        )

    async def test_buildings_update_non_existing(self, uow):
        with pytest.raises(NotFoundError):
            await service.update_building(
                1, {"country": "Anglia", "address": "Graniczna 11"}, uow
            )
