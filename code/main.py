import fastapi

from .models import City
from .models import PostRequest
from .models import PollingStation
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
