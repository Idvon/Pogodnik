from pathlib import Path

from src.config_file_parser.file_parser import JSONParser, TOMLParser, create_parser

json_parser = create_parser(Path("example_config.json"))
toml_parser = create_parser(Path("example_config.toml"))
errored_parser = create_parser(Path("booba.dooba"))


def test_error_parser():
    assert isinstance(errored_parser, str)
    assert errored_parser == "Please, check extension file"


def test_json_geo_config():
    assert isinstance(json_parser, JSONParser)
    assert json_parser.get_geo_config() == {
        "city_name": "Saint Petersburg",
        "provider": "openweather",
        "api_key": "geo api key",
    }


def test_json_weather_config():
    assert isinstance(json_parser, JSONParser)
    assert json_parser.get_weather_config() == {
        "provider": "openweather",
        "api_key": "weather api key",
    }


def test_geo_configs_equal():
    assert isinstance(json_parser, JSONParser)
    assert isinstance(toml_parser, TOMLParser)
    assert json_parser.get_geo_config() == toml_parser.get_geo_config()


def test_weather_configs_equal():
    assert isinstance(json_parser, JSONParser)
    assert isinstance(toml_parser, TOMLParser)
    assert json_parser.get_weather_config() == toml_parser.get_weather_config()
