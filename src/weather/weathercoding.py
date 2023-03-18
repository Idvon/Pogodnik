from requests import get

from src.output.compas import direction


class WeatherProvider:
    url: str
    data: dict

    def request(self):
        return get(self.url).json()

    def weather_data(self, call):
        return self.data


class OpenWeatherWeatherProvider(WeatherProvider):
    def __init__(self, weather_config, coords):
        self.url = (
            "https://api.openweathermap.org/data/2.5/weather?"
            f"lat={coords['lat']}&lon={coords['lon']}&"
            f"appid={weather_config['api_key']}&"
            "units=metric&"
        )

    def weather_data(self, call):
        if call["cod"] != 200:
            return "Please, check weather API key"
        else:
            self.data = {
                "provider": "openweather",
                "temp": call["main"]["temp"],
                "hum": call["main"]["humidity"],
                "winddir": direction(call["wind"]["deg"]),
                "winddeg": call["wind"]["deg"],
                "windspeed": call["wind"]["speed"],
            }
            return super().weather_data(self.data)


class OpenMeteoWeatherProvider(WeatherProvider):
    def __init__(self, weather_config, coords):
        self.url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={coords['lat']}&longitude={coords['lon']}&"
            "current_weather=true&"
            "windspeed_unit=ms&"
            "hourly=relativehumidity_2m"
        )

    def weather_data(self, call):
        current_time = call["current_weather"]["time"]
        list_time = call["hourly"]["time"]
        index_humidity = list_time.index(current_time)
        self.data = {
            "provider": "openmeteo",
            "temp": call["current_weather"]["temperature"],
            "hum": call["hourly"]["relativehumidity_2m"][index_humidity],
            "winddir": direction(int(call["current_weather"]["winddirection"])),
            "winddeg": int(call["current_weather"]["winddirection"]),
            "windspeed": call["current_weather"]["windspeed"],
        }
        return super().weather_data(self.data)


PROVIDERS = {
    "openweather": OpenWeatherWeatherProvider,
    "openmeteo": OpenMeteoWeatherProvider,
}


def create_weather_provider(weather_config, coords):
    provider = weather_config["provider"]
    if provider in PROVIDERS.keys():
        return PROVIDERS[provider](weather_config, coords)
    else:
        return "Please, check weather provider name"
