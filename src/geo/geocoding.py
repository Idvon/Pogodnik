from requests import get
import json
from typing import Union


class GeoProvider:
    config: Union[dict, str, None]

    def get_coords(self) -> Union[dict, str]:
        if self.config is None:
            return "This city is not found. Please, check city name"
        elif self.config == "key":
            return "Invalid API key. Please, check API key"
        else:
            return {'name': self.config['name'],
                    'state': self.config['state'],
                    'country': self.config['country'],
                    'lat': self.config['lat'],
                    'lon': self.config['lon']}


class OpenWeatherGeoProvider(GeoProvider):

    def __init__(self, geo_config: dict):
        call = get("https://api.openweathermap.org/geo/1.0/direct?"
                   f"q={geo_config['city_name']}&"
                   f"appid={geo_config['api_key']}")
        data = json.loads(call.text)
        if type(data) is list:
            self.config = None if len(data) == 0 else data[0]
        else:
            self.config = "key"


extensions = {'openweather': OpenWeatherGeoProvider}


def geo(geo_config: dict) -> GeoProvider:
    extension = geo_config['provider']
    if extension in extensions.keys():
        return extensions[extension](geo_config)
