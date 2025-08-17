from datetime import datetime
from typing import NamedTuple


class GeoConfig(NamedTuple):
    provider: str
    limit: int
    api_key: str


class WeatherConfig(NamedTuple):
    provider: str
    api_key: str


class GeoData(NamedTuple):
    city: str
    country: str
    state: str | None


class Coords(NamedTuple):
    lat: float
    lon: float


class WeatherData(NamedTuple):
    datetime: datetime
    provider: str
    temp: float
    hum: int
    winddir: str
    winddeg: int
    windspeed: float


class CityData(NamedTuple):
    weather_data: WeatherData
    geo_data: GeoData
