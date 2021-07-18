import pytest

from mcollector.repository.buildings_repository import BuildingsRepository


@pytest.mark.asyncio
async def test_buildings_list(session, building):
    building1 = await building()
    building2 = await building()
    buildings = await BuildingsRepository(session).list()
    assert buildings == [building1, building2]
