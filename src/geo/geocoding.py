import abc
import aiohttp
from typing import Dict, Union, Optional

from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.structures import Coords, GeoConfig, GeoData


class GeoProvider(abc.ABC):
    response: Optional[dict]
    url: str
    payload: dict

    @abc.abstractmethod
    async def request(self, session: aiohttp.ClientSession) -> None:
        """
        Request geo data and return response
        """

    def get_coords(self) -> Coords:  # extraction of coordinates from the geo provider's response
        return Coords(self.response["lat"], self.response["lon"])

    def get_city_data(self) -> GeoData:  # extraction of city name and city country from the geo provider's response
        return GeoData(
            self.response["name"],
            self.response["country"],
            self.response.get("state", ""),
        )


class OpenWeatherGeoProvider(GeoProvider):
    def __init__(self, geo_config: GeoConfig, city_name: str):
        self.payload: Dict[str, Union[int, str]] = {
            "q": city_name,
            "limit": geo_config.limit,
            "appid": geo_config.api_key,
        }
        self.url = "https://api.openweathermap.org/geo/1.0/direct"

    async def request(self, session: aiohttp.ClientSession):
        async with session.get(self.url, params=self.payload) as response:
            self.response: list = await response.json()
            match self.response:
                case []:
                    raise ProviderNoDataError(
                        "This city is not found. Please, check city name"
                    )
                case {"cod": 401, **args}:
                    raise ProviderNoDataError("Please, check geo API key")
            self.response = self.response[0]


PROVIDERS = {"openweather": OpenWeatherGeoProvider}


def create_geo_provider(geo_config: GeoConfig, city_name: str) -> GeoProvider:
    provider = geo_config.provider
    if provider in PROVIDERS.keys():
        return PROVIDERS[provider](geo_config, city_name)
    raise ProviderCreationError("Please, check geo provider name")
