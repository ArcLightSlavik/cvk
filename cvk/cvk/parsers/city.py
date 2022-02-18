from typing import List
from typing import NamedTuple

from cvk.cvk.models import City
from cvk.cvk.models import PollingStation


def parse_city(city: List[NamedTuple]) -> List[City]:
    cities = []

    for data_columns in city:
        polling_station = PollingStation(
            identifier=data_columns[0],
            address=data_columns[2],
            streets=None
        )

        polling_city = City(
            identifier=1,
            name='',
            polling_stations=None
        )

        if '–' in data_columns[1]:
            city_and_address = data_columns[1].split('–', 1)
            split_address = city_and_address[1].split(';')
            polling_station_address = []

            for unique_address in split_address:
                if ',' in unique_address:
                    count = 0
                    for character in unique_address:
                        if character == ':':
                            break
                        elif character == ',':
                            count += 1
                    # BLACK FUCKING MAGIC! PLEASE DO NOT TOUCH!
                    address_split_list = [*map(str.strip, unique_address.split(',', maxsplit=count))]
                    for address_split in address_split_list:
                        polling_station_address.append(address_split)

            polling_station.streets = polling_station_address
            polling_city.name = city_and_address[0]
            polling_city.polling_stations = [polling_station]
            cities.append(polling_city)
        else:
            polling_city.polling_stations = [polling_station]
            if ',' in data_columns[1]:
                parts = data_columns[1].split(',')
                for part in parts:
                    polling_city.name = part
                    cities.append(polling_city)
            else:
                polling_city.name = data_columns[1]
                cities.append(polling_city)
    return cities
