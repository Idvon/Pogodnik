import pytest

from src.config_file_parser.file_parser import JSONParser, TOMLParser, create_parser

json_parser = create_parser("example_config.json", ".json")
toml_parser = create_parser("example_config.toml", ".toml")


def test_example_json():
    assert isinstance(json_parser, JSONParser)


def test_json_geo_config():
    assert json_parser.get_geo_config() == {
        "city_name": "Saint Petersburg",
        "provider": "openweather",
        "api_key": "geo api key",
    }


def test_json_weather_config():
    assert json_parser.get_weather_config() == {
        "provider": "openweather",
        "api_key": "weather api key",
    }


def test_geo_configs_equal():
    assert json_parser.get_geo_config() == toml_parser.get_geo_config()


def test_weather_configs_equal():
    assert json_parser.get_weather_config() == toml_parser.get_weather_config()


def test_example_toml():
    assert isinstance(toml_parser, TOMLParser)
