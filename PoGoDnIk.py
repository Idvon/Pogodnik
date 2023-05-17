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

FILE_CONFIG: Path
FILE_OUTPUT: Path


def parser_terminal():
    parser = argparse.ArgumentParser(description="Weather by config file")              # to run directly
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    global FILE_CONFIG, FILE_OUTPUT
    FILE_CONFIG = Path(args.config)
    FILE_OUTPUT = Path(args.output)


def parser_files(file_config: Path, file_output: Path):                                 # to run as a module
    global FILE_CONFIG, FILE_OUTPUT
    FILE_CONFIG = file_config
    FILE_OUTPUT = file_output
    return main()


def main():
    file_config = FILE_CONFIG
    file_output = FILE_OUTPUT
    file_db = Path("db.sqlite3")
    if not file_config.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(file_config)
    geo_config = config_parser.get_geo_config()
    weather_config = config_parser.get_weather_config()

    if file_db.is_file():                                                               # cache initialization
        timeout = config_parser.get_timeout()
        local_weather_provider = create_local_weather_provider(
            file_db, geo_config.city_name, timeout
        )
        try:
            weather_cache, geo_cache = local_weather_provider.weather_data()
            return to_display(weather_cache, geo_cache)
        except ProviderNoDataError:
            pass

    geo_provider = create_geo_provider(geo_config)                                      # geo data initialization
    coords = geo_provider.get_coords()
    geo_data = geo_provider.get_city_data()

    net_weather_provider = create_net_weather_provider(weather_config, coords)          # initializing the weather data
    weather_data = net_weather_provider.weather_data(net_weather_provider.request())    # of the net provider

    create_output_format(weather_data, geo_data, file_output).city_outputs()            # initialize output to a file
    create_output_format(weather_data, geo_data, file_db).city_outputs()                # initialize output to a db
    return to_display(weather_data, geo_data)                                           # initialize output to str form


if __name__ == "__main__":
    parser_terminal()
    print(main())
