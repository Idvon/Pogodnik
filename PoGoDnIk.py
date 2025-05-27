import argparse
import asyncio
import time
from pathlib import Path
from typing import Optional, Any, Union, Tuple

from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import create_output_format, to_display
from src.structures import GeoConfig, WeatherConfig, WeatherData, GeoData
from src.weather.providers.local import create_local_weather_provider
from src.weather.providers.network import create_net_weather_provider

FILE_DB = Path("db.sqlite3")


def get_cache(name: str, time_out: int) -> Union[Tuple[Any, Any] | None]:
    if FILE_DB.is_file():
        local_weather_provider = create_local_weather_provider(FILE_DB, name, time_out)
        try:
            weather_cache, geo_cache = local_weather_provider.weather_data()
            return weather_cache, geo_cache
        except ProviderNoDataError:
            pass


async def to_cache(weather_data: WeatherData, geo_data: GeoData, output_file: Path):

    async with asyncio.TaskGroup() as tg:
        task = tg.create_task(create_output_format(weather_data, geo_data, output_file))
        task2 = tg.create_task(create_output_format(weather_data, geo_data, FILE_DB))
        task = await task
        task2 = await task2
        task.city_outputs()
        task2.city_outputs()
"""    task = await create_output_format(  # initialize output to a file
        weather_data, geo_data, output_file
        )
    task2 = await create_output_format(  # initialize output to a db
        weather_data, geo_data, FILE_DB
        )
    task.city_outputs()
    task2.city_outputs()"""


async def main(
        config_geo: GeoConfig,
        config_weather: WeatherConfig,
        name_city: str,
        output_file: Path,
        num: int,
):
    geo_provider = create_geo_provider(config_geo, name_city)
    geo_provider.response = geo_provider.request()[num]
    coords = geo_provider.get_coords()
    geo_data = geo_provider.get_city_data()

    net_weather_provider = create_net_weather_provider(  # initializing the weather data
        config_weather, coords
    )
    weather_data = net_weather_provider.weather_data(  # of the net provider
        net_weather_provider.request()
    )
    # await to_cache(weather_data, geo_data, output_file)
    return weather_data, geo_data  # initialize output to str form


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
        data = cache
    else:
        data = asyncio.run(main(geo_config, weather_config, city_name, output, 0))
        asyncio.run(to_cache(data[0], data[1], output))

    print(to_display(data[0], data[1]))
    print(time.time() - start_time)
