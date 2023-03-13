import datetime
from requests import get
from typing import Optional
from src.output.compas import direction


class WeatherProvider:
    config:


class OpenWeatherWeatherProvider(WeatherProvider):

    def __init__(self, weather_config):



class OpenMeteoWeatherProvider(WeatherProvider):


extensions = {'openweather': OpenMeteoWeatherProvider,
              'openmeteo': OpenMeteoWeatherProvider}


def weather(weather_config):

