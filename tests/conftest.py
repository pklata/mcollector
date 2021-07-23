import asyncio
from typing import Callable

import pytest
from httpx import AsyncClient
from mcollector_tests.factories import BuildingFactory

from mcollector.db import DBManager
from mcollector.fastapi import app
from mcollector.locations.models import Local


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    DBManager.start_mappers()
    await DBManager.recreate_db()
    return DBManager.get_engine()


@pytest.fixture
async def recreate_db(async_engine):
    yield
    await DBManager.recreate_db()


@pytest.fixture
async def nested_session(async_engine, monkeypatch):
    """Nested session"""
    async with DBManager.session_factory() as session:

        def mock_session_factory():
            return session

        nested = await session.begin_nested()
        monkeypatch.setattr(DBManager, "session_factory", mock_session_factory)
        yield session
        await nested.rollback()


@pytest.fixture
def async_app():
    return AsyncClient(app=app, base_url="https://test")


@pytest.fixture
def building() -> Callable:
    return BuildingFactory


@pytest.fixture
def local():
    return Local(7)
