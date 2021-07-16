import pytest

from mcollector.repository.buildings_repository import BuildingsRepository


@pytest.mark.asyncio
async def test_buildings_list(session, building):
    async with session.begin():
        session.add(building)
        await session.commit()
    buildings = await BuildingsRepository(session).list()
    assert buildings == [building]
