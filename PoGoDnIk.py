import argparse
from src.weather import open_weather
from src.weather import open_meteo
from src.output import conclusion
from src.geo.geocoding import geo
from src.config_file_parser.file_parser import create_parser


def main():
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("--config", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    parser = create_parser(args.config)  # call parser
    city_data = geo(parser.get_geo_config()).get_coords()  # call geo_providers data
    weather_config = parser.get_weather_config()
    if type(city_data) is str:
        return city_data
    else:
        if weather_config['provider'] == "openweather":
            appid = weather_config['api_key']
            return conclusion.printing(open_weather.weather_data(city_data, appid), args.output)
        elif weather_config['provider'] == "openmeteo":
            return conclusion.printing(open_meteo.weather_data(city_data), args.output)
        else:
            return "Please, check provider name"


if __name__ == "__main__":
    print(main())
