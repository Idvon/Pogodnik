import argparse
from src.weather_providers import open_weather
from src.weather_providers import open_meteo
from src.output import conclusion
from src.geo_providers import geocoding
from src.config_file_parser import file_parser


def main():
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    parser = file_parser.create_parser(args.config)  # parser = JSONParser()
    city = geocoding.geo(parser.get_geo_config())
    weather_config = parser.get_weather_config()
    if city is None:
        return "This city is not found. Please, check city name"
    elif weather_config['provider'] == "openweather":
        appid = weather_config['api_key']
        return conclusion.printing(open_weather.weather_data(city, appid), args.output)
    elif weather_config['weather_provider']['name'] == "openmeteo":
        return conclusion.printing(open_meteo.weather_data(city), args.output)
    else:
        return "Please, check provider name"


if __name__ == "__main__":
    print(main())
