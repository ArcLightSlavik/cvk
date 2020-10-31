import json
import httpx
import pytest


@pytest.mark.asyncio
async def test_poll_stations(async_api: httpx.AsyncClient) -> None:
    response = await async_api.post('/poll_stations', json={'url': 'https://www.drv.gov.ua/ords/portal/!cm_core.cm_index?option=ext_dvk&pid100=46&pf3001=372&prejim=2'})
    response.raise_for_status()
    response_json = response.json()
    file = open('cvk/test_data/poll_station.json')
    assert response_json == json.load(file)


@pytest.mark.asyncio
async def test_constituencies(async_api: httpx.AsyncClient) -> None:
    response = await async_api.post('/constituencies', json={'url': 'https://www.cvk.gov.ua/pls/vm2020/pvm116pt001f01=695pt00_t001f01=695pid112=2pid100=46pid102=3634rej=0.html#'})
    response.raise_for_status()
    response_json = response.json()
    file = open('cvk/test_data/constituencies.json')
    assert response_json == json.load(file)


@pytest.mark.asyncio
async def test_candidates(async_api: httpx.AsyncClient) -> None:
    response = await async_api.post('/candidates', json={'url': 'https://www.cvk.gov.ua/pls/vm2020/pvm056pid102=63610pf7691=63610pt001f01=695rej=0pt00_t001f01=695.html#89a'})
    response.raise_for_status()
    response_json = response.json()
    file = open('cvk/test_data/candidates.json')
    assert response_json == json.load(file)
