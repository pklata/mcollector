import pytest
from httpx import AsyncClient

from mcollector.fastapi import app


@pytest.fixture
def async_app(session):
    return AsyncClient(app=app, base_url="https://test")
