import argparse
from pathlib import Path

from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import create_output_format, to_display
from src.weather.weathercoding import (
    create_local_weather_provider,
    create_net_weather_provider,
)


def parser_terminal():
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    return Path(args.config), Path(args.output)


def main(file_config: Path, file_output: Path):
    file_db = Path("db.sqlite3")
    if not file_config.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(file_config)
    geo_config = config_parser.get_geo_config()
    weather_config = config_parser.get_weather_config()

    if file_db.is_file():
        timeout = config_parser.get_timeout()
        local_weather_provider = create_local_weather_provider(
            file_db, geo_config.city_name, timeout
        )
        try:
            weather_cache, geo_cache = local_weather_provider.weather_data()
            return to_display(weather_cache, geo_cache)
        except ProviderNoDataError:
            pass

    geo_provider = create_geo_provider(geo_config)
    coords = geo_provider.get_coords()
    geo_data = geo_provider.get_city_data()

    net_weather_provider = create_net_weather_provider(weather_config, coords)
    weather_data = net_weather_provider.weather_data(net_weather_provider.request())

    create_output_format(weather_data, geo_data, file_output).city_outputs()
    create_output_format(weather_data, geo_data, file_db).city_outputs()
    return to_display(weather_data, geo_data)


if __name__ == "__main__":
    file_config, file_output = parser_terminal()
    print(main(file_config, file_output))
