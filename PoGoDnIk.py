import argparse
import datetime
from pathlib import Path
from typing import NamedTuple

from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import create_output_format, to_display
from src.weather.weathercoding import (
    create_local_weather_provider,
    create_net_weather_provider,
)


class CityData(NamedTuple):
    datetime: datetime.datetime
    provider: str
    temp: float
    hum: int
    winddir: str
    winddeg: int
    windspeed: float
    city: str
    state: str
    country: str


def main():
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    file_config = Path(args.config)
    file_out = Path(args.output)
    file_db = Path("db.sqlite3")
    if not file_config.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(file_config)
    geo_config = config_parser.get_geo_config()
    weather_config = config_parser.get_weather_config()

    if file_db.is_file():
        timeout = config_parser.get_timeout().timeout
        local_weather_provider = create_local_weather_provider(
            file_db, geo_config.city_name, timeout
        )
        try:
            cache = local_weather_provider.weather_data()
            return to_display(cache)
        except ProviderNoDataError:
            pass

    geo_provider = create_geo_provider(geo_config)
    coords = geo_provider.get_coords()
    geo_data = geo_provider.get_city_data()

    net_weather_provider = create_net_weather_provider(weather_config, coords)
    weather_data = net_weather_provider.weather_data(net_weather_provider.request())

    data = *weather_data, *geo_data
    city_data = CityData._make(data)
    create_output_format(city_data, file_out).weather_outputs()
    create_output_format(city_data, file_db).weather_outputs()
    return to_display(city_data)


if __name__ == "__main__":
    main()
