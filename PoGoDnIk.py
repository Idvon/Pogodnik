import argparse
import asyncio
import time
from pathlib import Path
from typing import List, Union, Tuple

from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import create_output_format, to_display
from src.structures import CityData, GeoConfig, WeatherConfig
from src.weather.providers.local import create_local_weather_provider
from src.weather.providers.network import create_net_weather_provider

FILE_DB = Path("db.sqlite3")


# get valid cache from DB file
def get_cache(city_list: List[str], time_out: int) -> List[Union[CityData, str]]:
    cache = []
    if FILE_DB.is_file():
        for city in city_list:
            local_weather_provider = create_local_weather_provider(
                FILE_DB, city, time_out
            )
            try:
                cache.append(
                    local_weather_provider.weather_data()
                )  # retrieve city cache data
            except ProviderNoDataError:
                cache.append(city)
    return cache


# transmission of city data to DB file and output file
async def to_cache(city_data: List[CityData], output_file: Path) -> None:
    # initialize output to a file
    await create_output_format(city_data, output_file).city_outputs()

    # initialize output to a db
    await create_output_format(city_data, FILE_DB).city_outputs()


# get network data one city
async def network_data(
    config_geo: GeoConfig, config_weather: WeatherConfig, name_city: str, num: int
) -> CityData:
    # initializing the geo data
    geo_provider = create_geo_provider(config_geo, name_city)
    await geo_provider.request()
    geo_provider.valid_response = geo_provider.response[num]
    coords = geo_provider.get_coords()
    geo_data = geo_provider.geo_data()

    # initializing the weather data
    net_weather_provider = create_net_weather_provider(config_weather, coords)
    await net_weather_provider.request()
    weather_data = net_weather_provider.weather_data()
    return CityData(weather_data, geo_data)


# get city data and cache data all cities
async def main(
    config_geo: GeoConfig,
    config_weather: WeatherConfig,
    list_city: List[Union[CityData, str]],
    num: int,
) -> Tuple[List[CityData], List[CityData]]:
    cache = []
    tasks = []
    results = []

    # create tasks for new data
    async with asyncio.TaskGroup() as tg:
        for city in list_city:
            if type(city) is str:
                city = tg.create_task(
                    network_data(config_geo, config_weather, city, num)
                )
            tasks.append(city)

    # resulting task
    for task in tasks:
        if type(task) is asyncio.Task:
            task = await asyncio.wait_for(task, timeout=None)
            cache.append(task)
        results.append(task)
    return results, cache


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
    cities = config_parser.get_city()
    cache_city_data = get_cache(cities, timeout)
    cities_data, cache_data = asyncio.run(
        main(geo_config, weather_config, cache_city_data, 0)
    )
    asyncio.run(to_cache(cache_data, output))
    print("\n".join([to_display(data) for data in cities_data]))  # print to console
    print(time.monotonic() - s_t)
