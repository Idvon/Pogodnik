from typing import Dict, Union, Optional

from requests import get

from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.structures import Coords, GeoConfig, GeoData


class GeoProvider:
    response: dict
    url: str
    payload: dict

    def request(self) -> Union[Optional[list], dict]:
        match get(self.url, params=self.payload).json():
            case []:
                raise ProviderNoDataError("This city is not found. Please, check city name")
            case {'cod': 401, **args}:
                raise ProviderNoDataError("Please, check geo API key")
            case list() as valid_list:
                return valid_list

    def get_coords(self) -> Coords:
        return Coords(self.response["lat"], self.response["lon"])

    def get_city_data(self) -> GeoData:
        return GeoData(
            self.response["name"], self.response["country"], self.response.get("state", "")
        )


class OpenWeatherGeoProvider(GeoProvider):
    def __init__(self, geo_config: GeoConfig, city_name: str):
        self.payload: Dict[str, Union[int, str]] = {
            "q": city_name,
            "limit": geo_config.limit,
            "appid": geo_config.api_key,
        }
        self.url = "https://api.openweathermap.org/geo/1.0/direct"


PROVIDERS = {"openweather": OpenWeatherGeoProvider}


def create_geo_provider(geo_config: GeoConfig, city_name: str) -> GeoProvider:
    provider = geo_config.provider
    if provider in PROVIDERS.keys():
        return PROVIDERS[provider](geo_config, city_name)
    raise ProviderCreationError("Please, check geo provider name")
