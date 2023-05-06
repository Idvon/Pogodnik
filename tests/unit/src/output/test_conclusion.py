from datetime import datetime, timezone
from unittest.mock import patch

from freezegun import freeze_time

from src.output.conclusion import DatabaseWriter
from tests.unit.constants import GEO_DATA, LOCAL_FILE, OW_WEATHER_DATA


@freeze_time("2023-01-01 00:00:00.000000+00:00")
@patch("src.output.conclusion.sqlite3")
def test_db_writer_city_data(mocked_connect):
    provider = DatabaseWriter(OW_WEATHER_DATA, GEO_DATA, LOCAL_FILE)

    provider.city_outputs()

    mc = mocked_connect.connect().cursor().execute
    mc.assert_any_call(
        """
                CREATE TABLE IF NOT EXISTS weather_results (
                datetime date,
                provider text,
                temp real,
                hum integer,
                winddir text,
                winddeg integer,
                windspeed real,
                city text,
                state text,
                country text)
                """
    )
    mc.assert_called_with(
        "INSERT INTO weather_results VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            datetime.now(timezone.utc),
            "openweather",
            298.48,
            64,
            "N",
            349,
            0.62,
            "London",
            "",
            "GB",
        ),
    )
