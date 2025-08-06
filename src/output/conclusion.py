import abc
import asyncio
import aiosqlite
import aiocsv
import aiofiles
from pathlib import Path
from typing import List

from src.exceptions import ProviderCreationError
from src.structures import GeoData, WeatherData, CityData


class RecordCityData(abc.ABC):
    def __init__(self, city_data: List[CityData], file_out: Path):
        self.city_data = city_data
        self.file_out = file_out

    @abc.abstractmethod
    async def city_outputs(self) -> None:
        """
        Data retrieval and output in different file formats
        """
        return None


class CSVFileWriter(RecordCityData):
    async def city_outputs(self):
        if self.file_out.is_file():
            headers = None
        else:
            headers = self.city_data[0].weather_data._fields + self.city_data[0].geo_data._fields
        values = [(*self.city_data[i].weather_data, *self.city_data[i].geo_data) for i in range(len(self.city_data))]
        async with aiofiles.open(self.file_out, "a", newline="") as f:
            writer = aiocsv.AsyncWriter(f)
            if headers is not None:
                await writer.writerow(headers)
            await writer.writerows(values)


class DatabaseWriter(RecordCityData):
    async def city_outputs(self):
        values = *self.weather_data, *self.geo_data
        try:
            async with aiosqlite.connect(self.file_out) as db:
                headers = """
                    CREATE TABLE IF NOT EXISTS weather_results (
                    datetime date,
                    provider text,
                    temp real,
                    hum integer,
                    winddir text,
                    winddeg integer,
                    windspeed real,
                    city text,
                    country text,
                    state text)
                    """
                async with db.execute(headers) as cursor:
                    await cursor.execute(
                        "INSERT INTO weather_results VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        values,
                    )
                await db.commit()
                await cursor.close()
        except aiosqlite.Error as error:
            print(f"Error connecting to DB {error}")
        finally:
            await db.close()


WRITER = {".csv": CSVFileWriter, ".sqlite3": DatabaseWriter}


def create_output_format(
    city_data: List[CityData], file_out: Path
) -> RecordCityData:
    form = file_out.suffix
    if form in WRITER.keys():
        return WRITER[form](city_data, file_out)
    raise ProviderCreationError("No local provider available")


def to_display(city_data: List[CityData]) -> List[str]:
    text = []
    for data in city_data:
        text.append(
            f"Weather in {data.geo_data.city}\n"
            f"Country: {data.geo_data.country}\n"
            f"State: {data.geo_data.state}\n"
            f"Temperature: {data.weather_data.temp} \N{degree sign}C\n"
            f"Humidity: {data.weather_data.hum} %\n"
            f"Wind speed: {data.weather_data.windspeed} m/s\n"
            f"Wind direction: {data.weather_data.winddir}\n"
            f"By {data.weather_data.provider}\n"
        )
    return text
