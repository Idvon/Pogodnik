import argparse
from pathlib import Path

from src.config_file_parser.file_parser import create_parser
from src.geo.geocoding import create_geo_provider
from src.output import conclusion
from src.weather.weathercoding import create_weather_provider


def main():
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    file_config = Path(args.config)
    if not file_config.is_file():
        return "Config file not found"
    config_parser = create_parser(file_config)  # parser call to write config
    if isinstance(config_parser, str):
        return config_parser
    geo_config = create_geo_provider(config_parser.get_geo_config())  # init geo config
    if isinstance(geo_config, str):
        return geo_config
    coords = geo_config.get_coords()  # getting city coordinates
    if isinstance(coords, str):
        return coords
    geo_data = geo_config.get_city_data()  # getting city data
    weather_config = config_parser.get_weather_config()  # init weather config
    weather_provider = create_weather_provider(weather_config, coords)
    if isinstance(weather_provider, str):
        return weather_provider
    weather_data = weather_provider.weather_data(weather_provider.request())
    if isinstance(weather_data, str):
        return weather_data
    return conclusion.printing(geo_data, weather_data, args.output)


if __name__ == "__main__":
    print(main())
