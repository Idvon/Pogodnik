from typing import Dict, Union

from requests import get

from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.structures import Coords, GeoConfig, GeoData


class GeoProvider:
    config: dict
    city_list: list

    def get_coords(self) -> Coords:
        return Coords(self.config["lat"], self.config["lon"])

    def get_city_data(self) -> GeoData:
        return GeoData(
            self.config["name"], self.config["country"], self.config.get("state", "")
        )


class OpenWeatherGeoProvider(GeoProvider):
    def __init__(self, geo_config: GeoConfig, city_name: str):
        payload: Dict[str, Union[int, str]] = {
            "q": city_name,
            "limit": geo_config.limit,
            "appid": geo_config.api_key,
        }
        url = "https://api.openweathermap.org/geo/1.0/direct"
        match get(url, params=payload).json():
            case []:
                raise ProviderNoDataError("This city is not found. Please, check city name")
            case {'cod': 401, **args}:
                raise ProviderNoDataError("Please, check geo API key")
            case list() as valid_list:
                self.city_list = valid_list


PROVIDERS = {"openweather": OpenWeatherGeoProvider}


def create_geo_provider(geo_config: GeoConfig, city_name: str) -> GeoProvider:
    provider = geo_config.provider
    if provider in PROVIDERS.keys():
        return PROVIDERS[provider](geo_config, city_name)
    raise ProviderCreationError("Please, check geo provider name")
