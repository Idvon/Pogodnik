import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Tuple

from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import create_output_format, to_display
from src.structures import GeoConfig, GeoData, WeatherConfig, WeatherData
from src.weather.providers.local import create_local_weather_provider
from src.weather.providers.network import create_net_weather_provider

FILE_DB = Path("db.sqlite3")


def get_cache(name: str, time_out: int) -> Any:
    delta = timedelta(minutes=time_out)
    current_time = datetime.now(timezone.utc)
    if FILE_DB.is_file():
        local_weather_provider = create_local_weather_provider(FILE_DB, name)
        try:
            (
                weather_cache,
                geo_cache,
            ) = local_weather_provider.weather_data()  # retrieve city cache data
            if (current_time - weather_cache.datetime) <= delta:
                return weather_cache, geo_cache
        except ProviderNoDataError:
            pass


def to_cache(
    weather_data: WeatherData, geo_data: GeoData, output_file: Path
) -> None:

    # initialize output to a file
    create_output_format(
        weather_data, geo_data, output_file
    ).city_outputs()

    # initialize output to a db
    create_output_format(
        weather_data, geo_data, FILE_DB
    ).city_outputs()


def main(
    config_geo: GeoConfig,
    config_weather: WeatherConfig,
    name_city: str,
) -> Tuple[WeatherData, GeoData]:
    geo_provider = create_geo_provider(config_geo, name_city)
    geo_provider.request()
    coords = geo_provider.get_coords()
    geo_data = geo_provider.get_city_data()  # initializing the geo data

    net_weather_provider = create_net_weather_provider(  # initializing the weather data
        config_weather, coords
    )
    weather_data = net_weather_provider.weather_data(  # of the net provider
        net_weather_provider.request()
    )
    return weather_data, geo_data  # initialize output city data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    config = Path(args.config)
    output = Path(args.output)

    # define variables from config
    if not config.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(config)
    geo_config = config_parser.get_geo_config()
    weather_config = config_parser.get_weather_config()
    timeout = config_parser.get_timeout()
    city_name = config_parser.get_city_name()

    # retrieve data from the local cache
    cache = get_cache(city_name, timeout)

    if cache:
        city_data = cache
    else:
        city_data = main(geo_config, weather_config, city_name)
        to_cache(city_data[0], city_data[1], output)

    print(to_display(city_data[0], city_data[1]))
