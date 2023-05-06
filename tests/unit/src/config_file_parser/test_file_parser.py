from pathlib import Path

from pytest import raises

from src.config_file_parser.file_parser import JSONParser, TOMLParser, create_parser
from src.exceptions import ProviderCreationError
from src.structures import GeoConfig, WeatherConfig

json_parser = create_parser(Path("example_config.json"))
toml_parser = create_parser(Path("example_config.toml"))


def test_error_parser():
    with raises(ProviderCreationError):
        errored_parser = create_parser(Path("booba.dooba"))


def test_json_geo_config():
    assert isinstance(json_parser, JSONParser)
    assert json_parser.get_geo_config() == GeoConfig(
        "Saint Petersburg",
        "openweather",
        "geo api key",
    )


def test_json_weather_config():
    assert isinstance(json_parser, JSONParser)
    assert json_parser.get_weather_config() == WeatherConfig(
        "openweather",
        "weather api key",
    )


def test_geo_configs_equal():
    assert isinstance(json_parser, JSONParser)
    assert isinstance(toml_parser, TOMLParser)
    assert json_parser.get_geo_config() == toml_parser.get_geo_config()


def test_weather_configs_equal():
    assert isinstance(json_parser, JSONParser)
    assert isinstance(toml_parser, TOMLParser)
    assert json_parser.get_weather_config() == toml_parser.get_weather_config()


def test_timeout_equal():
    assert isinstance(json_parser, JSONParser)
    assert isinstance(toml_parser, TOMLParser)
    assert json_parser.get_timeout() == toml_parser.get_timeout()
