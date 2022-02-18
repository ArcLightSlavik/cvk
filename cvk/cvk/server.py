import httpx
import pandas

from fastapi.exceptions import HTTPException

from .chrome_session import ChromeSession


async def get_dataframe_from_url(url: str) -> list[pandas.DataFrame]:
    async with httpx.AsyncClient() as client:
        page = await client.get(url)
        if page.status_code != 200:
            raise HTTPException(status_code=400, detail='Internal request failed')
        dataframe_list = pandas.read_html(page.text)
        return dataframe_list


async def get_dataframe_from_selenium(url: str) -> list[pandas.DataFrame]:
    async with ChromeSession() as driver:
        driver.get(url)
        dataframe_list = pandas.read_html(driver.page_source)
        return dataframe_list
