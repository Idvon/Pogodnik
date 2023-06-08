import argparse
from pathlib import Path

from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import GeoProvider, create_geo_provider
from src.output.conclusion import create_output_format, to_display
from src.structures import Coords, GeoConfig, GeoData, WeatherConfig
from src.weather.weathercoding import (
    create_local_weather_provider,
    create_net_weather_provider,
)

FILE_CONFIG: Path
FILE_OUTPUT: Path
WEATHER_CONFIG: WeatherConfig
GEO_DATA: GeoData
GEO_CONFIG: GeoConfig
GEO_PROVIDER: GeoProvider
COORDS: Coords
TIMEOUT: int


def parser_terminal():
    parser = argparse.ArgumentParser(
        description="Weather by config file"
    )  # to run directly
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    global FILE_CONFIG, FILE_OUTPUT
    FILE_CONFIG = Path(args.config)
    FILE_OUTPUT = Path(args.output)


def parser_files(file_config: Path, file_output: Path):  # to run as a module
    global FILE_CONFIG, FILE_OUTPUT
    FILE_CONFIG = file_config
    FILE_OUTPUT = file_output


def get_config():
    if not FILE_CONFIG.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(FILE_CONFIG)
    global GEO_CONFIG, WEATHER_CONFIG, TIMEOUT
    GEO_CONFIG = config_parser.get_geo_config()
    WEATHER_CONFIG = config_parser.get_weather_config()
    TIMEOUT = config_parser.get_timeout()


# getting a list of cities
def get_city_list() -> dict:
    city_data: dict = dict()
    global GEO_PROVIDER, GEO_CONFIG
    GEO_PROVIDER = create_geo_provider(GEO_CONFIG)
    list_city = GEO_PROVIDER.list_city
    for city in list_city:
        city_data[
            list_city.index(city) + 1
        ] = f"name: {city['name']}, country: {city['country']}, state: {city['state']}"
    return city_data


def get_city_geo_data(number: int):
    global GEO_PROVIDER, COORDS, GEO_DATA
    GEO_PROVIDER.config = GEO_PROVIDER.list_city[number]
    COORDS = GEO_PROVIDER.get_coords()
    GEO_DATA = GEO_PROVIDER.get_city_data()


def main():
    file_db = Path("db.sqlite3")
    if file_db.is_file():  # cache initialization
        local_weather_provider = create_local_weather_provider(
            file_db, GEO_CONFIG.city_name, TIMEOUT
        )
        try:
            weather_cache, geo_cache = local_weather_provider.weather_data()
            return to_display(weather_cache, geo_cache)
        except ProviderNoDataError:
            pass

    net_weather_provider = create_net_weather_provider(
        WEATHER_CONFIG, COORDS
    )  # initializing the weather data
    weather_data = net_weather_provider.weather_data(
        net_weather_provider.request()
    )  # of the net provider

    create_output_format(
        weather_data, GEO_DATA, FILE_OUTPUT
    ).city_outputs()  # initialize output to a file
    create_output_format(
        weather_data, GEO_DATA, file_db
    ).city_outputs()  # initialize output to a db
    return to_display(weather_data, GEO_DATA)  # initialize output to str form


if __name__ == "__main__":
    parser_terminal()
    get_config()
    city_list = get_city_list()
    print("\n".join([f"{elem}. {city_list[elem]}" for elem in city_list]))
    num = int(input("Please write number your city: "))
    get_city_geo_data(num - 1)
    print(main())
