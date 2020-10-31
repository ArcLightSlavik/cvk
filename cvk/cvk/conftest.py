import httpx
import pytest
import fastapi.testclient

from . import main


@pytest.fixture
def api() -> fastapi.testclient.TestClient:
    return fastapi.testclient.TestClient(main.app)


@pytest.fixture
def async_api() -> httpx.AsyncClient:
    return httpx.AsyncClient(app=main.app, base_url="http://test")
