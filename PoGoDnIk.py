import argparse
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Tuple, Optional, Union, List, Coroutine, Set

from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import create_output_format, to_display
from src.structures import GeoConfig, GeoData, WeatherConfig, WeatherData, CityData
from src.weather.providers.local import create_local_weather_provider
from src.weather.providers.network import create_net_weather_provider

FILE_DB = Path("db.sqlite3")


def get_cache(city_list: List[str], time_out: int) -> Union[List[CityData], List[str]]:
    cache = []
    if FILE_DB.is_file():
        for city in city_list:
            local_weather_provider = create_local_weather_provider(FILE_DB, city, time_out)
            try:
                cache.append(local_weather_provider.weather_data())  # retrieve city cache data
            except ProviderNoDataError:
                cache.append(city)
    print("getcach", time.monotonic())
    return cache


async def to_cache(
    city_data: List[CityData], output_file: Path
) -> None:

    # initialize output to a file
    await create_output_format(
        city_data, output_file
    ).city_outputs()
    print("csv", time.monotonic())
    # initialize output to a db
    #await create_output_format(
    #    city_data, FILE_DB
    #).city_outputs()
    #print("db", time.monotonic())


async def async_exec(
    config_geo: GeoConfig,
    config_weather: WeatherConfig,
    list_city: List[str],
    time_out: int,
    output_file: Path
) -> List[CityData]:

    cache = []
    tasks = []
    results = []
    #cache_tasks = [tg.create_task(get_cache(city, time_out)) for city in list_city]
    #tasks = [await asyncio.wait_for(task, timeout=None) for task in cache_tasks]
    #i = 0

    async with asyncio.TaskGroup() as tg:
        for city in list_city:
            if type(city) is str:
                tasks.append(tg.create_task(main(config_geo, config_weather, city)))
        #tasks = [tg.create_task(main(config_geo, config_weather, city)) if type(city) is str else city for city in list_city]
    for task in tasks:
        if type(task) is asyncio.Task:
            result = await asyncio.wait_for(task, timeout=None)
            results.append(result)
            cache.append(result)
    await to_cache(cache, output_file)
    #results = [await asyncio.wait_for(task, timeout=None) if type(task) is asyncio.Task else task for task in tasks]
    """
    for city in list_city:
        if type(city) is not str:
            results.append(city)
        else:
            geo_provider = create_geo_provider(config_geo, city)
            await geo_provider.request()
            coords = geo_provider.get_coords()
            geo_data = geo_provider.get_city_data()

            # initializing the weather data
            net_weather_provider = create_net_weather_provider(
                config_weather, coords
            )
            await net_weather_provider.request()
            weather_data = net_weather_provider.weather_data()

            #caching.append(tg.create_task(to_cache(weather_data, geo_data, output_file)))
            results.append(CityData(weather_data, geo_data))
            cache.append(CityData(weather_data, geo_data))
            """
        #if tasks[i] is None:
        #    tasks[i] = tg.create_task(main(config_geo, config_weather, city))
        #    caching.append(tasks[i])
        #else:
        #    pass
        #i += 1
    #cache = [await asyncio.wait_for(task, timeout=None) for task in tasks]
    #task_caching = [tg.create_task(to_cache(weather_data, geo_data, output_file)) for weather_data, geo_data in cache]
    #await to_cache(cache, output_file)
    #results = [await asyncio.wait_for(task, timeout=None) if type(task) is asyncio.Task else task for task in tasks]
    return results


async def main(
    config_geo: GeoConfig,
    config_weather: WeatherConfig,
    name_city: str
) -> CityData:

    # initializing the geo data
    geo_provider = create_geo_provider(config_geo, name_city)
    await geo_provider.request()
    coords = geo_provider.get_coords()
    geo_data = geo_provider.get_city_data()

    # initializing the weather data
    net_weather_provider = create_net_weather_provider(
        config_weather, coords
    )
    await net_weather_provider.request()
    weather_data = net_weather_provider.weather_data()
    #to_cache(weather_data, geo_data, output_file)
    return CityData(weather_data, geo_data)  # initialize output city data


if __name__ == "__main__":
    s_t = time.monotonic()
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)   # add optional flag
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
    cities = config_parser.get_city()
    if type(cities) is not list:
        cities = [cities]
    cache_city_data = get_cache(cities, timeout)  # cache and cities name
    # print(cache_city_data)
    cities_data = asyncio.run(async_exec(geo_config, weather_config, cache_city_data, timeout, output))
    print(cities_data)
    # print('\n'.join([to_display(city_data[0], city_data[1]) for city_data in cities_data]))

    print(s_t)
    print(time.monotonic() - s_t)
    """
    sequential processing of a single city took 0.8...1.0 sec
    sequential processing of a cities took (0.9...1.2) * quantity cities sec
    """
