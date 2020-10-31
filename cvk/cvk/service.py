from typing import List
from typing import NamedTuple

import re

from .models import City
from .models import County
from .models import Candidate
from .models import PollingStation


def order_data_into_classes(data_tuple_list: List[NamedTuple]) -> List[City]:
    cities = []

    for data_columns in data_tuple_list:
        polling_station = PollingStation(
            identifier=data_columns[0],
            name='',
            description='',
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


def county_data_split(county_tuple_list: List[NamedTuple]) -> List[County]:
    counties = []
    for index, item in enumerate(county_tuple_list):
        if index is 0:
            continue

        a_county = County(
            identifier=int(item[0]),
            name=item[1],
            streets=item[3]
        )
        counties.append(a_county)

    return counties


def candidates_data_split(candidates_tuple: List[NamedTuple]) -> List[Candidate]:
    candidates_list = []
    party = None
    for index, item in enumerate(candidates_tuple):
        # skip initial table
        if index is 0:
            continue
        # get the party
        if item[1] == item[2]:
            party = item[1]
            continue

        # country number can be either int or 'First Candidate'
        try:
            number_in_country = int(item[5])
        except ValueError :
            number_in_country = item[5]

        # Weird spacing issue fix
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
        candidates_list.append(a_candidate)

    return candidates_list
