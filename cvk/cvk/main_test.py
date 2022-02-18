import json
import httpx
import pytest


@pytest.mark.asyncio
async def test_poll_stations(async_api: httpx.AsyncClient) -> None:
    response = await async_api.post('/poll_stations')
    response.raise_for_status()
    response_json = response.json()
    file = open('cvk/test_data/poll_station.json')
    assert response_json == json.load(file)
    file.close()


@pytest.mark.asyncio
async def test_constituencies(async_api: httpx.AsyncClient) -> None:
    response = await async_api.post('/constituencies')
    response.raise_for_status()
    response_json = response.json()
    file = open('cvk/test_data/constituencies.json')
    assert response_json == json.load(file)
    file.close()


@pytest.mark.asyncio
async def test_candidates(async_api: httpx.AsyncClient) -> None:
    response = await async_api.post('/candidates')
    response.raise_for_status()
    response_json = response.json()
    file = open('cvk/test_data/candidates.json')
    assert response_json == json.load(file)
    file.close()
