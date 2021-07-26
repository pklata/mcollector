from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory, LocalFactory

from mcollector.errors import NotFoundError
from mcollector.locations import service


@pytest.mark.asyncio
@pytest.mark.usefixtures("recreate_db")
class TestLocationsService:
    async def test_buildings_list(self, building, session, uow):
        building1 = building()
        building2 = building()
        session.add(building1)
        session.add(building2)
        await session.commit()
        buildings = await service.list_buildings(uow)
        assert buildings == [asdict(building1), asdict(building2)]

    async def test_buildings_get(self, building, session, uow):
        building1 = building(id=1)
        session.add(building1)
        await session.commit()
        building_ = await service.get_building(1, uow)
        assert building_ == asdict(building1)

    async def test_buildings_get_non_existing(self, uow):
        with pytest.raises(NotFoundError) as e:
            await service.get_building(1, uow)
        assert e.value.message == "Building with id: 1 not found."

    async def test_buildings_add(self, uow):
        building1 = BuildingFactory()
        result = await service.add_building(asdict(building1), uow)
        buildings = await service.list_buildings(uow)
        building1.id = result["id"]
        assert result == {"id": 1}
        assert buildings == [asdict(building1)]

    async def test_buildings_delete(self, building, session, uow):
        session.add(building(id=1))
        await session.commit()
        await service.delete_building(1, uow)
        buildings = await service.list_buildings(uow)
        assert buildings == []

    async def test_buildings_delete_non_existing(self, uow):
        with pytest.raises(NotFoundError) as e:
            await service.delete_building(1, uow)
        assert e.value.message == "Building with id: 1 not found."

    async def test_buildings_update(self, session, building, uow):
        session.add(building())
        await session.commit()
        result = await service.update_building(
            1, {"country": "Anglia", "address": "Graniczna 11"}, uow
        )
        assert result == {"id": 1}
        assert (await service.get_building(1, uow)) == {
            "address": "Graniczna 11",
            "city": "Warszawa",
            "country": "Anglia",
            "county": "mazowieckie",
            "id": 1,
            "zip_code": "02-200",
        }

    async def test_buildings_update_non_existing(self, uow):
        with pytest.raises(NotFoundError):
            await service.update_building(
                1, {"country": "Anglia", "address": "Graniczna 11"}, uow
            )

    async def test_locals_list(self, building, session, uow, locals_setup):
        locals_ = await service.list_locals(1, uow)
        assert locals_ == [asdict(locals_setup[0]), asdict(locals_setup[1])]

    async def test_locals_get(self, building, session, uow, locals_setup):
        building_ = await service.get_local(1, uow)
        assert building_ == asdict(locals_setup[1])

    async def test_locals_get_non_existing(self, uow):
        with pytest.raises(NotFoundError) as e:
            await service.get_local(1, uow)
        assert e.value.message == "Local with id: 1 not found."

    async def test_locals_add(self, uow):
        local = LocalFactory()
        result = await service.add_local(2, asdict(local), uow)
        assert result == {"id": 1}
        locals_ = await service.list_locals(2, uow)
        assert locals_ == [
            {"building_id": 2, "description": None, "id": 1, "number": 7}
        ]

    async def test_locals_delete(self, building, session, uow, locals_setup):
        await service.delete_local(1, uow)
        locals_ = await service.list_locals(1, uow)
        assert locals_ == [asdict(locals_setup[0])]

    async def test_locals_delete_non_existing(self, uow):
        with pytest.raises(NotFoundError) as e:
            await service.delete_local(1, uow)
        assert e.value.message == "Local with id: 1 not found."

    async def test_locals_update(self, session, uow, locals_setup):
        result = await service.update_local(
            1, {"number": 17, "description": "Lokal Usługowy"}, uow
        )
        assert result == {"id": 1}
        assert await service.get_local(1, uow) == {
            "building_id": 1,
            "description": "Lokal Usługowy",
            "id": 1,
            "number": 17,
        }

    async def test_locals_update_non_existing(self, uow):
        with pytest.raises(NotFoundError):
            await service.update_building(
                1, {"country": "Anglia", "address": "Graniczna 11"}, uow
            )
