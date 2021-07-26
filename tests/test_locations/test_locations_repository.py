from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory, LocalFactory

from mcollector.errors import NotFoundError
from mcollector.locations.repository import LocationsRepository


@pytest.mark.asyncio
async def test_buildings_list(session, building):
    building1 = building()
    building2 = building()
    session.add(building1)
    session.add(building2)
    buildings = await LocationsRepository(session).list_buildings()
    assert buildings == [building1, building2]


@pytest.mark.asyncio
async def test_buildings_get(session, building):
    building1 = building(id=1)
    session.add(building1)
    await session.commit()
    building_ = await LocationsRepository(session).get_building(1)
    assert building_ == building1


@pytest.mark.asyncio
async def test_buildings_get_non_existing(session):
    with pytest.raises(NotFoundError):
        await LocationsRepository(session).get_building(1)


@pytest.mark.asyncio
async def test_buildings_add(session):
    building1 = BuildingFactory()
    _id = await LocationsRepository(session).add_building(asdict(building1))
    buildings = await LocationsRepository(session).list_buildings()
    building1.id = _id
    assert _id == 1
    assert buildings == [building1]


@pytest.mark.asyncio
async def test_building_delete(session, building):
    session.add(building(id=1))
    await session.commit()
    await LocationsRepository(session).delete_building(1)
    buildings = await LocationsRepository(session).list_buildings()
    assert buildings == []


@pytest.mark.asyncio
async def test_building_delete_non_existing(session, building):
    with pytest.raises(NotFoundError) as e:
        await LocationsRepository(session).delete_building(1)
    assert e.value.message == "Building with id: 1 not found."


@pytest.mark.asyncio
async def test_buildings_update(session, building):
    _building = building(id=1)
    session.add(_building)
    await session.commit()
    _id = await LocationsRepository(session).update_building(
        1, country="Anglia", address="Graniczna 11"
    )
    assert _id == 1
    assert asdict(_building) == {
        "address": "Graniczna 11",
        "city": "Warszawa",
        "country": "Anglia",
        "county": "mazowieckie",
        "id": 1,
        "zip_code": "02-200",
    }


@pytest.mark.asyncio
async def test_buildings_update_non_existing(session):
    with pytest.raises(NotFoundError) as e:
        await LocationsRepository(session).update_building(
            1, country="Anglia", address="Graniczna 11"
        )
    assert e.value.message == "Building with id: 1 not found."


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


@pytest.mark.asyncio
async def test_locals_list(session, locals_setup):
    locals_ = await LocationsRepository(session).list_locals(1)
    assert locals_ == locals_setup


@pytest.mark.asyncio
async def test_locals_get(session, building, local, locals_setup):
    local = await LocationsRepository(session).get_local(1)
    assert local == locals_setup[1]


@pytest.mark.asyncio
async def test_locals_get_non_existing(session):
    with pytest.raises(NotFoundError) as e:
        await LocationsRepository(session).get_local(1)
    assert e.value.message == "Local with id: 1 not found."


@pytest.mark.asyncio
async def test_locals_add(session):
    local = LocalFactory()
    _id = await LocationsRepository(session).add_local(1, asdict(local))
    local_ = await LocationsRepository(session).get_local(1)
    local.id = _id
    assert local_.building_id == 1
    assert local_.number == local.number
    assert local_.description == local.description


@pytest.mark.asyncio
async def test_local_delete(session, building, locals_setup):
    await LocationsRepository(session).delete_local(1)
    buildings = await LocationsRepository(session).list_locals(1)
    assert buildings == [locals_setup[0]]


@pytest.mark.asyncio
async def test_local_delete_non_existing(session, building):
    with pytest.raises(NotFoundError) as e:
        await LocationsRepository(session).delete_local(1)
    assert e.value.message == "Local with id: 1 not found."


@pytest.mark.asyncio
async def test_local_update(session, building, locals_setup):
    _id = await LocationsRepository(session).update_local(
        1, number=17, description="Lokal Usługowy"
    )
    assert _id == 1
    assert asdict(locals_setup[1]) == {
        "building_id": 1,
        "description": "Lokal Usługowy",
        "id": 1,
        "number": 17,
    }


@pytest.mark.asyncio
async def test_local_update_non_existing(session):
    with pytest.raises(NotFoundError) as e:
        await LocationsRepository(session).update_local(
            1, number=17, description="Lokal Usługowy"
        )
    assert e.value.message == "Local with id: 1 not found."
