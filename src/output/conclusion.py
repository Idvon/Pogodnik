import abc
import sqlite3
from pathlib import Path
from typing import List

import aiocsv
import aiofiles
import aiosqlite

from src.exceptions import ProviderCreationError
from src.structures import CityData


class RecordCityData(abc.ABC):  # base class for record city data
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
            headers = (
                self.city_data[0].weather_data._fields
                + self.city_data[0].geo_data._fields
            )
        values = [
            (*self.city_data[i].weather_data, *self.city_data[i].geo_data)
            for i in range(len(self.city_data))
        ]
        async with aiofiles.open(self.file_out, "a", newline="") as f:
            writer = aiocsv.AsyncWriter(f)
            if headers is not None:
                await writer.writerow(headers)
            await writer.writerows(values)


class DatabaseWriter(RecordCityData):
    async def city_outputs(self):
        values = [
            (*self.city_data[i].weather_data, *self.city_data[i].geo_data)
            for i in range(len(self.city_data))
        ]
        try:
            db = await aiosqlite.connect(self.file_out)
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
            cursor = await db.cursor()
            await cursor.execute(headers)
            await cursor.executemany(
                "INSERT INTO weather_results VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                values,
            )
            await db.commit()
            await cursor.close()
        except sqlite3.Error as error:
            print(f"Error connecting to DB {error}")
        finally:
            await db.close()


WRITER = {".csv": CSVFileWriter, ".sqlite3": DatabaseWriter}


def create_output_format(city_data: List[CityData], file_out: Path) -> RecordCityData:
    form = file_out.suffix
    if form in WRITER.keys():
        return WRITER[form](city_data, file_out)
    raise ProviderCreationError("No local provider available")


def to_display(
    city_data: CityData,
) -> str:  # converting received city data into text strings
    return (
        f"Weather in {city_data.geo_data.city}\n"
        f"Country: {city_data.geo_data.country}\n"
        f"State: {city_data.geo_data.state}\n"
        f"Temperature: {city_data.weather_data.temp} \N{degree sign}C\n"
        f"Humidity: {city_data.weather_data.hum} %\n"
        f"Wind speed: {city_data.weather_data.windspeed} m/s\n"
        f"Wind direction: {city_data.weather_data.winddir}\n"
        f"By {city_data.weather_data.provider}\n"
    )
