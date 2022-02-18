import os

import fastapi

from cvk.cvk.models import City, County, Candidate

from cvk.cvk.server import get_dataframe_from_selenium
from cvk.cvk.server import get_dataframe_from_url
from cvk.cvk.pandas_converter import pandas_converter

from cvk.cvk.parsers.city import parse_city
from cvk.cvk.parsers.county import parse_county
from cvk.cvk.parsers.candidates import parse_candidates


app = fastapi.FastAPI()


@app.post("/poll_stations")
async def post_polling_stations() -> dict[str, list[City]]:
    tables = await get_dataframe_from_url(os.environ["POLL_STATION_URL"])
    return {
        'ordinary': parse_city(pandas_converter(tables[0])),
        'special': parse_city(pandas_converter(tables[1]))
    }


@app.post('/constituencies')
async def post_constituencies() -> list[County]:
    dataframe_list = await get_dataframe_from_selenium(os.environ["CONSTITUENSIES_URL"])
    table = pandas_converter(dataframe_list[2])
    return parse_county(table)


@app.post('/candidates')
async def post_candidates() -> list[Candidate]:
    dataframe_list = await get_dataframe_from_selenium(os.environ["CANDIDATES_URL"])
    table = pandas_converter(dataframe_list[4])
    return parse_candidates(table)
