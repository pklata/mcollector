from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from mcollector.db import DBManager
from mcollector.locations.repository import LocationsRepository


class LocationsUnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self) -> "LocationsUnitOfWork":
        self.session: AsyncSession = self.session_factory()
        self.locations = LocationsRepository(self.session)
        return self

    async def __aexit__(self, exn_type: Any, exn_value: Any, traceback: Any) -> None:
        if exn_type is not None:
            print(f"Exception: {exn_type}, {exn_value}, {traceback}")
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


def uow_factory() -> LocationsUnitOfWork:
    return LocationsUnitOfWork(DBManager.session_factory)
