import abc
from typing import Optional

from requests import get

from src.structures import WeatherData


class WeatherProvider(abc.ABC):
    url: str
    payload: dict

    def request(self) -> Optional[dict]:
        return get(self.url, params=self.payload).json()

    @abc.abstractmethod
    def weather_data(self, response: Optional[dict]) -> WeatherData:
        """
        Parse response and return data structure
        """
        return WeatherData._make({})
