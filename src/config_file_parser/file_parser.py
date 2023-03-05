import json
import toml
import pathlib


class ConfigFileParser:
    config: dict

    def get_geo_config(self) -> dict:  # get geo data
        return {'city_name': self.config['city_name'],
                'provider': self.config['geo_provider']['name'],
                'api_key': self.config['geo_provider']['api_key']}

    def get_weather_config(self) -> dict:  # get weather data
        return {'provider': self.config['weather_provider']['name'],
                'api_key': self.config['weather_provider']['api_key']}


class JSONParser(ConfigFileParser):

    def __init__(self, f):
        self.config = json.load(f)  # load json from f(file)


class TOMLParser(ConfigFileParser):

    def __init__(self, f):
        self.config = toml.load(f)  # load toml from f(file)


def create_parser(file_name: str) -> ConfigFileParser:
    extensions = {".json": JSONParser,
                  ".toml": TOMLParser}
    extension = pathlib.Path(file_name).suffix
    if extension in extensions.keys():
        with open(file_name) as f:
            return extensions[extension](f)