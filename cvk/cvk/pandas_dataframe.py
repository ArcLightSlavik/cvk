from typing import List
from typing import NamedTuple

import pandas

from fastapi.exceptions import HTTPException

from .session import session
from .httpx_client import HTTPX_client


async def get_tables_from_url(url: str) -> List[pandas.DataFrame]:
    async with HTTPX_client.get_client() as client:
        page = await client.get(url)
        if page.status_code != 200:
            raise HTTPException(status_code=400, detail='Internal request failed')
        dataframe_list = pandas.read_html(page.text)
        return dataframe_list


async def do_selenium(url: str) -> List[pandas.DataFrame]:
    async with session() as driver:
        driver.get(url)
        dataframe_list = pandas.read_html(driver.page_source)
        return dataframe_list


def pandas_data_to_tuple(dataframe: pandas.DataFrame) -> List[NamedTuple]:
    data_tuple_list = []

    for data_tuple in dataframe.itertuples(index=False):
        data_tuple_list.append(data_tuple)
    return data_tuple_list
