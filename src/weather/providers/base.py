import abc
import aiohttp
from typing import Optional

from src.structures import WeatherData


class WeatherProvider(abc.ABC):  # base class for network weather providers
    response: Optional[dict]
    url: str
    payload: dict

    async def request(self) -> None:  # request and record weather data from a network provider's
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.payload) as response:
                self.response = await response.json()

    @abc.abstractmethod
    def weather_data(self) -> WeatherData:
        """
        Parse response and return data structure
        """
        return WeatherData._make(self.response)
