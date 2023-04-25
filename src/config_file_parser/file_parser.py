import json
from pathlib import Path
from typing import NamedTuple, TextIO

import toml

from src.exceptions import ProviderCreationError


class GeoConfig(NamedTuple):
    city_name: str
    provider: str
    api_key: str


class WeatherConfig(NamedTuple):
    provider: str
    api_key: str


class Timeout(NamedTuple):
    timeout: int


class ConfigFileParser:
    config: dict

    def get_geo_config(self) -> GeoConfig:  # formation of geo config
        return GeoConfig(
            self.config["city_name"],
            self.config["geo_provider"]["name"],
            self.config["geo_provider"]["api_key"],
        )

    def get_weather_config(self) -> WeatherConfig:  # formation of weather config
        return WeatherConfig(
            self.config["weather_provider"]["name"],
            self.config["weather_provider"]["api_key"],
        )

    def get_timeout(self) -> Timeout:
        return Timeout(self.config["timeout"])


class JSONParser(ConfigFileParser):
    def __init__(self, f: TextIO):
        self.config = json.load(f)  # load json from f(file)


class TOMLParser(ConfigFileParser):
    def __init__(self, f: TextIO):
        self.config = toml.load(f)  # load toml from f(file)


EXTENSIONS = {".json": JSONParser, ".toml": TOMLParser}


def create_parser(file_name: Path) -> ConfigFileParser:
    extension = file_name.suffix
    if extension in EXTENSIONS.keys():
        with open(file_name) as f:
            return EXTENSIONS[extension](f)
    raise ProviderCreationError("Please, check file extension")
