import json
from pathlib import Path
from typing import TextIO, Union

import toml

from src.exceptions import ProviderCreationError


class ConfigFileParser:
    config: dict

    def get_geo_config(self) -> dict:  # formation of geo config
        return {
            "city_name": self.config["city_name"],
            "provider": self.config["geo_provider"]["name"],
            "api_key": self.config["geo_provider"]["api_key"],
        }

    def get_weather_config(self) -> dict:  # formation of weather config
        return {
            "provider": self.config["weather_provider"]["name"],
            "api_key": self.config["weather_provider"]["api_key"],
        }

    def get_timeout(self) -> dict:
        return {"timeout": self.config["timeout"]}


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
