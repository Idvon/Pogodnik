from typing import NamedTuple

from requests import get

from src.config_file_parser.file_parser import GeoConfig
from src.exceptions import ProviderCreationError, ProviderNoDataError


class GeoData(NamedTuple):
    city: str
    state: str
    country: str


class Coords(NamedTuple):
    lat: float
    lon: float


class GeoProvider:
    config: dict

    def get_coords(self) -> Coords:
        if len(self.config) == 0:
            raise ProviderNoDataError("This city is not found. Please, check city name")
        if self.config.get("cod") is not None:
            raise ProviderNoDataError("Please, check geo API key")
        return Coords(self.config["lat"], self.config["lon"])

    def get_city_data(self) -> GeoData:
        return GeoData(
            self.config["name"], self.config.get("state", ""), self.config["country"]
        )


class OpenWeatherGeoProvider(GeoProvider):
    def __init__(self, geo_config: GeoConfig):
        payload = {"q": geo_config.city_name, "appid": geo_config.api_key}
        url = "https://api.openweathermap.org/geo/1.0/direct"
        data = get(url, params=payload).json()
        if isinstance(data, list):
            self.config = dict() if len(data) == 0 else data[0]
        else:
            self.config = data


PROVIDERS = {"openweather": OpenWeatherGeoProvider}


def create_geo_provider(geo_config: GeoConfig) -> GeoProvider:
    provider = geo_config.provider
    if provider in PROVIDERS.keys():
        return PROVIDERS[provider](geo_config)
    raise ProviderCreationError("Please, check geo provider name")
