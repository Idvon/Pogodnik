from requests import get

from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.structures import Coords, GeoConfig, GeoData


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
            self.config["name"], self.config["country"], self.config.get("state", "")
        )


class OpenWeatherGeoProvider(GeoProvider):
    def __init__(self, geo_config: GeoConfig):
        payload = {"q": geo_config.city_name, "limit": geo_config.limit, "appid": geo_config.api_key}
        url = "https://api.openweathermap.org/geo/1.0/direct"
        data = get(url, params=payload).json()
        for city in data:
            print(f"{data.index(city) + 1}. name: {city['name']}, country: {city['country']}, state: {city['state']}")
        num_city = int(input("Please write number your city: "))
        self.config = data[num_city - 1]


PROVIDERS = {"openweather": OpenWeatherGeoProvider}


def create_geo_provider(geo_config: GeoConfig) -> GeoProvider:
    provider = geo_config.provider
    if provider in PROVIDERS.keys():
        return PROVIDERS[provider](geo_config)
    raise ProviderCreationError("Please, check geo provider name")
