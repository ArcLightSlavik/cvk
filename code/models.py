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
