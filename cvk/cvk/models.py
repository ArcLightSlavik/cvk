import typing
import pydantic


class PostRequest(pydantic.BaseModel):
    url: str


class PollingStation(pydantic.BaseModel):
    identifier: int
    name: str
    description: str
    address: str
    streets: typing.List[typing.Any]


class City(pydantic.BaseModel):
    identifier: int
    name: str
    polling_stations: typing.List[PollingStation]


class County(pydantic.BaseModel):
    identifier: int
    name: str
    streets: typing.Any


class Candidate(pydantic.BaseModel):
    party_identifier: int
    full_name: str
    birthday_and_place_of_birth: str
    info: str
    county: typing.Union[str, int]
    number_in_county: typing.Union[int, str]
    party: str
