import re
import pandas
import fastapi

from .models import City
from .models import County
from .models import Candidate
from .models import PostRequest
from .models import PollingStation
from .session import session
from .pandas_dataframe import get_tables_from_url
from .pandas_dataframe import pandas_data_to_tuple


app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/stuff")
async def read_item(post_request: PostRequest):
    tables = await get_tables_from_url(post_request.url)
    ordinary_table = pandas_data_to_tuple(tables[0])
    special_table = pandas_data_to_tuple(tables[1])
    ordinary_data = order_data_into_classes(ordinary_table)
    special_data = order_data_into_classes(special_table)
    return {'ordinary': ordinary_data, 'special': special_data}


@app.post('/stuff_two')
async def a_driver(post_request: PostRequest):
    dataframe_list = await do_selenium(post_request.url)
    ordinary_table = pandas_data_to_tuple(dataframe_list[2])
    the_return = do_everything(ordinary_table)
    return the_return


@app.post('/candidates')
async def candidates(post_request: PostRequest):
    dataframe_list = await do_selenium(post_request.url)
    ordinary_table = pandas_data_to_tuple(dataframe_list[4])
    the_return = do_everything_else(ordinary_table)
    return the_return


def do_everything_else(tuple_list):
    candidates_list = []
    party = None
    for index, item in enumerate(tuple_list):
        if index is 0:
            continue
        if item[1] == item[2]:
            party = item[1]
            continue

        try:
            number_in_country = int(item[5])
        except Exception:
            number_in_country = item[5]

        full_name = re.sub(r"(\w)([А-ЯҐЄІЇ])", r"\1 \2", item[1])

        a_candidate = Candidate(
            party_identifier=int(item[0]),
            full_name=full_name,
            birthday_and_place_of_birth=item[2],
            info=item[3],
            county=item[4],
            number_in_county=number_in_country,
            party=party
        )
        # if a_candidate.county == 'Перший кандидат' or a_candidate.county == '9':
        candidates_list.append(a_candidate)

    return candidates_list


def do_everything(tuple_list):
    counties = []
    for index, item in enumerate(tuple_list):
        if index is 0:
            continue

        a_county = County(
            identifier=int(item[0]),
            name=item[1],
            streets=item[3]
        )
        counties.append(a_county)

    return counties


async def do_selenium(url):
    async with session() as driver:
        driver.get(url)
        dataframe_list = pandas.read_html(driver.page_source)
        return dataframe_list


def order_data_into_classes(data_tuple_list):
    cities = []

    for data_columns in data_tuple_list:
        if '–' in data_columns[1]:
            city_and_address = data_columns[1].split('–', 1)
            split_address = city_and_address[1].split(';')
            polling_station_address = []

            for unique_address in split_address:
                if ',' in unique_address:
                    count = 0
                    for ch in unique_address:
                        if ch == ':':
                            break
                        elif ch == ',':
                            count += 1
                    # BLACK FUCKING MAGIC! PLEASE DO NOT TOUCH!
                    some_list = [*map(str.strip, unique_address.split(',', maxsplit=count))]
                    for value in some_list:
                        polling_station_address.append(value)

            polling_station_addressed = PollingStation(
                identifier=data_columns[0],
                name='',
                description='',
                address=data_columns[2],
                streets=polling_station_address
            )

            a_city = City(
                identifier=1,
                name=city_and_address[0],
                polling_stations=[polling_station_addressed]
            )
            cities.append(a_city)
        else:
            polling_station_not_addressed = PollingStation(
                identifier=data_columns[0],
                name='',
                description='',
                address=data_columns[2],
                streets=[]
            )

            if ',' in data_columns[1]:
                parts = data_columns[1].split(',')
                for part in parts:
                    a_city = City(
                        identifier=1,
                        name=part.strip(),
                        polling_stations=[polling_station_not_addressed]
                    )
                    cities.append(a_city)
            else:
                a_city = City(
                    identifier=1,
                    name=data_columns[1],
                    polling_stations=[polling_station_not_addressed]
                )
                cities.append(a_city)
    return cities
