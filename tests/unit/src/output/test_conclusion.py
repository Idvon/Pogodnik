from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from freezegun import freeze_time

from src.output.conclusion import DatabaseWriter
from tests.unit.constants import LIST_CITY_DATA, LOCAL_FILE


@freeze_time("2023-01-01 00:00:00.000000+00:00")
@patch("src.output.conclusion.aiosqlite", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_db_writer_city_data(mocked_connect):
    provider = DatabaseWriter(LIST_CITY_DATA, LOCAL_FILE)

    await provider.city_outputs()

    mce = await mocked_connect.connect()
    mce = await mce.cursor()
    mce = mce.execute
    mcem = await mocked_connect.connect()
    mcem = await mcem.cursor()
    mcem = mcem.executemany
    mce.assert_any_call(
        """
                CREATE TABLE IF NOT EXISTS weather_results (
                datetime date,
                provider text,
                status text,
                temp real,
                hum integer,
                winddir text,
                winddeg integer,
                windspeed real,
                clouds integer,
                precipitation real,
                cityid integer,
                city text,
                country text,
                state text)
                """
    )
    mcem.assert_called_with(
        "INSERT INTO weather_results VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                datetime.now(timezone.utc),
                "openweather",
                "Rain",
                298.74,  # hella hot
                64,
                "N",
                349,
                0.62,
                100,
                3.16,
                3163858,
                "London",
                "GB",
                "England",
            ),
            (
                datetime.now(timezone.utc),
                "openmeteo",
                "Clouds",
                11.5,
                76,
                "NE",
                30,
                2.2,
                76,
                0.0,
                None,
                "London",
                "GB",
                "England",
            ),
        ],
    )
