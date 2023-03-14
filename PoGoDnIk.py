import argparse
import json

import toml

from src import open_meteo, open_weather
from src.conclusion import printing
from src.geocoding import geo


def main():
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    with open(args.config) as f:
        if args.config.endswith("json"):
            config_data = json.load(f)
        elif args.config.endswith("toml"):
            config_data = toml.load(f)
    geo_data = {'city_name': config_data['city_name'],
                'api_key': config_data['geo_provider']['api_key']}
    city = geo(geo_data)
    if city is None:
        return "This city is not found. Please, check city name"
    elif config_data['weather_provider']['name'] == "openweather":
        appid = config_data['weather_provider']['api_key']
        return printing(open_weather.weather_data(city, appid), args.output)
    elif config_data['weather_provider']['name'] == "openmeteo":
        return printing(open_meteo.weather_data(city), args.output)
    else:
        return "Please, check provider name"


if __name__ == "__main__":
    print(main())
