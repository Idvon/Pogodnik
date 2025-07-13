import json
from pathlib import Path
from typing import TextIO, List, Union

import toml

from src.exceptions import ProviderCreationError
from src.structures import GeoConfig, WeatherConfig


class ConfigFileParser:
    config: dict

    def get_geo_config(self) -> GeoConfig:  # formation of geo config
        return GeoConfig(
            self.config["geo_provider"]["name"],
            self.config["geo_provider"]["limit"],
            self.config["geo_provider"]["api_key"],
        )

    def get_weather_config(self) -> WeatherConfig:  # formation of weather config
        return WeatherConfig(
            self.config["weather_provider"]["name"],
            self.config["weather_provider"]["api_key"],
        )

    def get_timeout(self) -> int:  # obtaining a time-out between weather queries
        return self.config["timeout"]

    def get_city(self) -> Union[List[str], str]:  # obtaining a city name
        return self.config["city_name"]


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
