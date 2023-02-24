import json
import open_weather
import conclusion
import open_meteo
import geocoding


def main():
    with open("config.json") as f:
        config_data = json.load(f)
    city = geocoding.geo(config_data)
    if city is None:
        return "This city is not found. Please, check city name"
    elif config_data['provider_name'] == "openweather":
        return conclusion.printing(open_weather.weather_data(city))
    elif config_data['provider_name'] == "openmeteo":
        return conclusion.printing(open_meteo.weather_data(city))
    return "Please, check provider name"


if __name__ == "__main__":
    print(main())
