import argparse
from pathlib import Path

from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output import conclusion
from src.weather.weathercoding import (
    create_local_weather_provider,
    create_net_weather_provider,
)


def main():
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    file_config = Path(args.config)
    file_out = Path(args.output)
    if not file_config.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(file_config)

    if file_out.is_file():
        timeout = int(config_parser.get_timeout()["timeout"])
        local_weather_provider = create_local_weather_provider(file_out, timeout)
        try:
            cache = local_weather_provider.weather_data()
            return conclusion.printing(cache)
        except ProviderNoDataError:
            pass

    geo_config = create_geo_provider(config_parser.get_geo_config())
    coords = geo_config.get_coords()
    geo_data = geo_config.get_city_data()

    weather_config = config_parser.get_weather_config()
    net_weather_provider = create_net_weather_provider(weather_config, coords)
    weather_data = net_weather_provider.weather_data(net_weather_provider.request())

    city_data = weather_data | geo_data
    conclusion.to_file(city_data, file_out)
    conclusion.sql_file(city_data)
    return conclusion.printing(city_data)


if __name__ == "__main__":
    main()
