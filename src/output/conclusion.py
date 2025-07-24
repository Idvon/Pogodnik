import abc
import asyncio
import aiosqlite
import aiocsv
import aiofiles
from pathlib import Path

from src.exceptions import ProviderCreationError
from src.structures import GeoData, WeatherData


class CityData(abc.ABC):
    def __init__(self, weather_data: WeatherData, geo_data: GeoData, file_out: Path):
        self.weather_data = weather_data
        self.geo_data = geo_data
        self.file_out = file_out

    @abc.abstractmethod
    async def city_outputs(self) -> dict:
        """
        Data retrieval and output in different file formats
        """
        return {}


class CSVFileWriter(CityData):
    async def city_outputs(self):
        headers = self.weather_data._fields + self.geo_data._fields
        values = *self.weather_data, *self.geo_data
        async with aiofiles.open(self.file_out, "w+", newline="") as f:
            reader = aiocsv.AsyncDictReader(f, headers)
            writer = aiocsv.AsyncDictWriter(f, headers)
            if await reader.get_fieldnames() == headers:
                await writer.writerow(headers)
            #await f.flush()
        async with aiofiles.open(self.file_out, "a", newline="") as f:
            await f.flush()
            writer = aiocsv.AsyncWriter(f)
            await writer.writerow(values)
            #await f.close()


class DatabaseWriter(CityData):
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
    weather_data: WeatherData, geo_data: GeoData, file_out: Path
) -> CityData:
    form = file_out.suffix
    if form in WRITER.keys():
        return WRITER[form](weather_data, geo_data, file_out)
    raise ProviderCreationError("No local provider available")


def to_display(weather_data: WeatherData, geo_data: GeoData) -> str:
    return (
        f"Weather in {geo_data.city}\n"
        f"Country: {geo_data.country}\n"
        f"State: {geo_data.state}\n"
        f"Temperature: {weather_data.temp} \N{degree sign}C\n"
        f"Humidity: {weather_data.hum} %\n"
        f"Wind speed: {weather_data.windspeed} m/s\n"
        f"Wind direction: {weather_data.winddir}\n"
        f"By {weather_data.provider}\n"
    )
