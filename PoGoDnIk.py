import argparse
import asyncio
import time
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
            weather_cache, geo_cache = local_weather_provider.weather_data()  # retrieve city cache data
            if (current_time - weather_cache.datetime) <= delta:
                return weather_cache, geo_cache
        except ProviderNoDataError:
            pass


async def to_cache(
    weather_data: WeatherData, geo_data: GeoData, output_file: Path
) -> None:
    async with asyncio.TaskGroup() as tg:

        # initialize output to a file
        to_out_file = tg.create_task(
            create_output_format(weather_data, geo_data, output_file)
        )
        task = await to_out_file
        task.city_outputs()

        # initialize output to a db
        to_db_file = tg.create_task(
            create_output_format(weather_data, geo_data, FILE_DB)
        )
        task2 = await to_db_file
        task2.city_outputs()


async def main(
    config_geo: GeoConfig,
    config_weather: WeatherConfig,
    name_city: str,
    num: int,
) -> Tuple[WeatherData, GeoData]:
    geo_provider = create_geo_provider(config_geo, name_city)
    geo_provider.response = geo_provider.request()[num]
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
    start_time = time.time()
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
        city_data = asyncio.run(main(geo_config, weather_config, city_name, 0))
        asyncio.run(to_cache(city_data[0], city_data[1], output))

    print(to_display(city_data[0], city_data[1]))
    print(time.time() - start_time)
