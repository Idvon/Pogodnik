COORDS = {"lon": 10.99, "lat": 44.34}
OW_RESPONSE = {
    "coord": COORDS,
    "weather": [
        {
            "id": 501,
            "main": "Rain",
            "description": "moderate rain",
            "icon": "10d",
        }
    ],
    "base": "stations",
    "main": {
        "temp": 298.48,
        "feels_like": 298.74,
        "temp_min": 297.56,
        "temp_max": 300.05,
        "pressure": 1015,
        "humidity": 64,
        "sea_level": 1015,
        "grnd_level": 933,
    },
    "visibility": 10000,
    "wind": {"speed": 0.62, "deg": 349, "gust": 1.18},
    "rain": {"1h": 3.16},
    "clouds": {"all": 100},
    "dt": 1661870592,
    "sys": {
        "type": 2,
        "id": 2075663,
        "country": "IT",
        "sunrise": 1661834187,
        "sunset": 1661882248,
    },
    "timezone": 7200,
    "id": 3163858,
    "name": "Zocca",
    "cod": 200,
}

OM_RESPONSE = {
    "current_weather": {
        "time": "2022-01-01T02:00",
        "temperature": 2.4,
        "weathercode": 3,
        "windspeed": 11.9,
        "winddirection": 95.0,
    },
    "hourly": {
        "time": ["2022-01-01T00:00", "2022-01-01T01:00", "2022-01-01T02:00"],
        "windspeed_10m": [3.16, 3.02, 3.3],
        "temperature_2m": [13.7, 13.3, 12.8],
        "relativehumidity_2m": [82, 83, 86],
    },
}
