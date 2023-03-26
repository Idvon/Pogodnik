import json

from requests import get

from src.exceptions import ProviderCreationError, ProviderNoDataError


class GeoProvider:
    config: dict

    def get_coords(self) -> dict:
        if len(self.config) == 0:
            raise ProviderCreationError(
                "This city is not found. Please, check city name"
            )
        if self.config.get("cod") is not None:
            raise ProviderNoDataError("Please, check weather API key")
        return {"lat": self.config["lat"], "lon": self.config["lon"]}

    def get_city_data(self) -> dict:
        return {
            "city": self.config["name"],
            "state": self.config["state"],
            "country": self.config["country"],
        }


class OpenWeatherGeoProvider(GeoProvider):
    def __init__(self, geo_config: dict):
        call = get(
            "https://api.openweathermap.org/geo/1.0/direct?"
            f"q={geo_config['city_name']}&"
            f"appid={geo_config['api_key']}"
        )
        data = json.loads(call.text)
        if isinstance(data, list):
            self.config = dict() if len(data) == 0 else data[0]
        else:
            self.config = data


PROVIDERS = {"openweather": OpenWeatherGeoProvider}


def create_geo_provider(geo_config: dict) -> GeoProvider:
    provider = geo_config["provider"]
    if provider in PROVIDERS.keys():
        return PROVIDERS[provider](geo_config)
    raise ProviderCreationError("Please, check geo provider name")
