import json
from typing import Union

from requests import get


class GeoProvider:
    config: dict

    def get_coords(self) -> Union[dict, str]:
        if len(self.config) == 0:
            return "This city is not found. Please, check city name"
        elif self.config.get("cod") is not None:
            return "Invalid API key. Please, check geo API key"
        else:
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


def create_geo_provider(geo_config: dict) -> Union[GeoProvider, str]:
    provider = geo_config["provider"]
    if provider in PROVIDERS.keys():
        return PROVIDERS[provider](geo_config)
    else:
        return "Please, check geo provider name"
