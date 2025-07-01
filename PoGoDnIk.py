import argparse
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Tuple, Optional

from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import create_output_format, to_display
from src.structures import GeoConfig, GeoData, WeatherConfig, WeatherData
from src.weather.providers.local import create_local_weather_provider
from src.weather.providers.network import create_net_weather_provider

FILE_DB = Path("db.sqlite3")


def get_cache(name: str, time_out: int) -> Optional[Tuple[WeatherData, GeoData]]:
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


async def main(
    config_geo: GeoConfig,
    config_weather: WeatherConfig,
    name_city: str,
) -> Tuple[WeatherData, GeoData]:
    tasks = []
    results = []
    async with aiohttp.ClientSession() as session:
        # initializing the geo data
        geo_provider = create_geo_provider(config_geo, name_city)
        await geo_provider.request(session)
        coords = geo_provider.get_coords()
        geo_data = geo_provider.get_city_data()

        # initializing the weather data
        net_weather_provider = create_net_weather_provider(
            config_weather, coords
        )
        await net_weather_provider.request(session)
        weather_data = net_weather_provider.weather_data()

    return weather_data, geo_data  # initialize output city data


async def asyn(geo_config, weather_config, cities):
    tasks = []
    results = []
    async with asyncio.TaskGroup() as tg:
        for city in cities:
            tasks.append(tg.create_task(main(geo_config, weather_config, city)))
    async for task in asyncio.as_completed(tasks):
        results.append(await task)
        #results = asyncio.as_completed(tasks)
        #task.add_done_callback(tasks.discard)
    #print(tasks)

    return results


if __name__ == "__main__":
    s_t = time.monotonic()
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
    cities = config_parser.get_city_list()
    call_cities = list()

    # retrieve data from the local cache
    #cache = get_cache(cities, timeout)
    #if cache:
        #city_data = cache
    #else:
        #call_cities.append(city)
    #print(call_cities)
    cities_data = asyncio.run(asyn(geo_config, weather_config, cities))
    #print(type(cities_data))
    #[to_cache(city_data[0], city_data[1], output) for city_data in cities_data]
    print('\n'.join([to_display(city_data[0], city_data[1]) for city_data in cities_data]))
    #print(city_data)
        #print(to_display(city_data[0], city_data[1]))

    print(time.monotonic() - s_t)
    """
    sequential processing of a single city took 0.8...1.0 sec
    sequential processing of a cities took (0.9...1.2) * quantity cities sec
    """
