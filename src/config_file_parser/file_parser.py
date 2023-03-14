import json
import toml
import pathlib
from typing import Union


class ConfigFileParser:
    config: dict

    def get_geo_config(self) -> dict:  # get geo_providers data
        return {'city_name': self.config['city_name'],
                'provider': self.config['geo_provider']['name'],
                'api_key': self.config['geo_provider']['api_key']}

    def get_weather_config(self) -> dict:  # get weather data
        return {'provider': self.config['weather_provider']['name'],
                'api_key': self.config['weather_provider']['api_key']}


class JSONParser(ConfigFileParser):

    def __init__(self, f: [Union[str, bytes]]):
        self.config = json.load(f)  # load json from f(file)


class TOMLParser(ConfigFileParser):

    def __init__(self, f: [Union[str, bytes]]):
        self.config = toml.load(f)  # load toml from f(file)


extensions = {'.json': JSONParser,
              '.toml': TOMLParser}


def create_parser(file_name: str) -> ConfigFileParser:
    extension = pathlib.Path(file_name).suffix
    if extension in extensions.keys():
        with open(file_name) as f:
            return extensions[extension](f)
