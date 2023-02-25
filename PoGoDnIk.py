import json
import toml
import open_weather
import conclusion
import open_meteo
import geocoding
import argparse


def main():
    parser = argparse.ArgumentParser(description="Weather by config file")
    parser.add_argument("Filename", type=str)
    file_name = parser.parse_args()
    if file_name.Filename.count("json") == 1:
        with open("config.json") as f:
            config_data = json.load(f)
    elif file_name.Filename.count("toml") == 1:
        with open("config.toml") as f:
            config_data = toml.load(f)
    city = geocoding.geo(config_data)
    if city is None:
        return "This city is not found. Please, check city name"
    elif config_data['weather_provider']['name'] == "openweather":
        appid = config_data['weather_provider']['api_key']
        return conclusion.printing(open_weather.weather_data(city, appid))
    elif config_data['weather_provider']['name'] == "openmeteo":
        return conclusion.printing(open_meteo.weather_data(city))
    return "Please, check provider name"


if __name__ == "__main__":
    print(main())
