import abc
import aiohttp
from typing import Optional, Coroutine

from src.structures import WeatherData


class WeatherProvider(abc.ABC):
    response: Optional[dict]
    url: str
    payload: dict

    async def request(self, session: aiohttp.ClientSession) -> None:
        async with session.get(self.url, params=self.payload) as response:
            self.response = await response.json()

    @abc.abstractmethod
    def weather_data(self) -> WeatherData:
        """
        Parse response and return data structure
        """
        return WeatherData._make(self.response)
