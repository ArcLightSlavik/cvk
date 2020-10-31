from typing import Dict
from typing import List

import fastapi

from .models import City
from .models import County
from .models import Candidate
from .models import PostRequest

from .service import county_data_split
from .service import candidates_data_split
from .service import order_data_into_classes

from .pandas_dataframe import do_selenium
from .pandas_dataframe import get_tables_from_url
from .pandas_dataframe import pandas_data_to_tuple


app = fastapi.FastAPI()


@app.post("/poll_stations")
async def post_polling_stations(post_request: PostRequest) -> Dict[str, List[City]]:
    tables = await get_tables_from_url(post_request.url)
    ordinary_table = pandas_data_to_tuple(tables[0])
    special_table = pandas_data_to_tuple(tables[1])
    ordinary_data = order_data_into_classes(ordinary_table)
    special_data = order_data_into_classes(special_table)
    return {'ordinary': ordinary_data, 'special': special_data}


@app.post('/constituencies')
async def post_constituencies(post_request: PostRequest) -> List[County]:
    dataframe_list = await do_selenium(post_request.url)
    table = pandas_data_to_tuple(dataframe_list[2])
    return county_data_split(table)


@app.post('/candidates')
async def post_candidates(post_request: PostRequest) -> List[Candidate]:
    dataframe_list = await do_selenium(post_request.url)
    table = pandas_data_to_tuple(dataframe_list[4])
    return candidates_data_split(table)
