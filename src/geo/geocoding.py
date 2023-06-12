from typing import Dict, Union

from requests import get

from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.structures import Coords, GeoConfig, GeoData


class GeoProvider:
    config: dict
    list_city: list

    def get_coords(self) -> Coords:
        return Coords(self.config["lat"], self.config["lon"])

    def get_city_data(self) -> GeoData:
        return GeoData(
            self.config["name"], self.config["country"], self.config.get("state", "")
        )


class OpenWeatherGeoProvider(GeoProvider):
    def __init__(self, geo_config: GeoConfig):
        payload: Dict[str, Union[int, str]] = {
            "q": geo_config.city_name,
            "limit": geo_config.limit,
            "appid": geo_config.api_key,
        }
        url = "https://api.openweathermap.org/geo/1.0/direct"
        self.list_city = get(url, params=payload).json()
        if len(self.list_city) == 0:
            raise ProviderNoDataError("This city is not found. Please, check city name")
        if (isinstance(self.list_city, dict)) and (self.list_city["cod"] is not None):
            raise ProviderNoDataError("Please, check geo API key")


PROVIDERS = {"openweather": OpenWeatherGeoProvider}


def create_geo_provider(geo_config: GeoConfig) -> GeoProvider:
    provider = geo_config.provider
    if provider in PROVIDERS.keys():
        return PROVIDERS[provider](geo_config)
    raise ProviderCreationError("Please, check geo provider name")
