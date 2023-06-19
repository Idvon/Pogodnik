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


# to run directly
def parser_terminal():
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    config = Path(args.config)
    output = Path(args.output)
    return config, output


def get_config(config: Path):
    if not config.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(config)
    get_geo_config = config_parser.get_geo_config()
    get_weather_config = config_parser.get_weather_config()
    get_timeout = config_parser.get_timeout()
    return get_geo_config, get_weather_config, get_timeout


# getting a list of cities
def get_city_list(config: GeoConfig):
    provider = create_geo_provider(config)
    list_city = provider.city_list
    town_list = dict()
    for city in list_city:
        town_list[
            list_city.index(city) + 1
        ] = f"name: {city['name']}, country: {city['country']}, state: {city['state']}"
    return provider, town_list


def get_city_geo_data(provider: GeoProvider, number: int):
    provider.config = provider.city_list[number]
    get_coords = provider.get_coords()
    get_city_data = provider.get_city_data()
    return get_coords, get_city_data


def main(
    config_geo: GeoConfig,
    config_weather: WeatherConfig,
    crd: Coords,
    data_geo: GeoData,
    output_file: Path,
    time_out: int,
):
    # cache initialization
    file_db = Path("db.sqlite3")
    if file_db.is_file():
        local_weather_provider = create_local_weather_provider(
            file_db, config_geo.city_name, time_out
        )
        try:
            weather_cache, geo_cache = local_weather_provider.weather_data()
            return to_display(weather_cache, geo_cache)
        except ProviderNoDataError:
            pass

    net_weather_provider = create_net_weather_provider(  # initializing the weather data
        config_weather, crd
    )
    weather_data = net_weather_provider.weather_data(  # of the net provider
        net_weather_provider.request()
    )

    create_output_format(  # initialize output to a file
        weather_data, data_geo, output_file
    ).city_outputs()
    create_output_format(  # initialize output to a db
        weather_data, data_geo, file_db
    ).city_outputs()
    return to_display(weather_data, data_geo)  # initialize output to str form


if __name__ == "__main__":
    file_config, file_output = parser_terminal()
    geo_config, weather_config, timeout = get_config(file_config)
    geo_provider = create_geo_provider(geo_config)
    coords, city_geo_data = get_city_geo_data(geo_provider, 0)
    print(main(geo_config, weather_config, coords, city_geo_data, file_output, timeout))
