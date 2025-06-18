import abc
from typing import Optional

from requests import get

from src.structures import WeatherData


class WeatherProvider(abc.ABC):
    response: Optional[dict]
    url: str
    payload: dict

    def request(self) -> None:
        self.response = get(self.url, params=self.payload).json()

    @abc.abstractmethod
    def weather_data(self) -> WeatherData:
        """
        Parse response and return data structure
        """
        return WeatherData._make(self.response)
