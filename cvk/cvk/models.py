from typing import Any
from typing import List
from typing import Union

import pydantic


class PollingStation(pydantic.BaseModel):
    identifier: int
    address: str
    streets: Union[List[Any], None]


class City(pydantic.BaseModel):
    identifier: int
    name: str
    polling_stations: Union[List[PollingStation], None]


class County(pydantic.BaseModel):
    identifier: int
    name: str
    streets: Any


class Candidate(pydantic.BaseModel):
    party_identifier: int
    full_name: str
    birthday_and_place_of_birth: str
    info: str
    county: Union[int, str]
    number_in_county: Union[int, str]
    party: str
