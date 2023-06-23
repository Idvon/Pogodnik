import argparse
from pathlib import Path

from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import create_output_format, to_display
from src.structures import WeatherConfig, GeoConfig
from src.weather.weathercoding import (
    create_local_weather_provider,
    create_net_weather_provider,
)


def get_cache(name: str, time_out: int, db: Path):
    if db.is_file():
        local_weather_provider = create_local_weather_provider(
            db, name, time_out
        )
        try:
            weather_cache, geo_cache = local_weather_provider.weather_data()
            return to_display(weather_cache, geo_cache)
        except ProviderNoDataError:
            pass


def main(
    config_geo: GeoConfig,
    config_weather: WeatherConfig,
    name_city: str,
    output_file: Path,
    db: Path,
    num: int
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

    create_output_format(  # initialize output to a file
        weather_data, geo_data, output_file
    ).city_outputs()
    create_output_format(  # initialize output to a db
        weather_data, geo_data, db
    ).city_outputs()
    return to_display(weather_data, geo_data)  # initialize output to str form


if __name__ == "__main__":
    file_db = Path("db.sqlite3")
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    config = Path(args.config)
    output = Path(args.output)

    if not config.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(config)
    geo_config = config_parser.get_geo_config()
    weather_config = config_parser.get_weather_config()
    timeout = config_parser.get_timeout()
    city_name = config_parser.get_city_name()

    cache = get_cache(city_name, timeout, file_db)
    if cache:
        print(cache)
    else:
        print(main(geo_config, weather_config, city_name, output, file_db, 0))
