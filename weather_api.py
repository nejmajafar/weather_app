import requests

from cities import CITIES

API_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherAPIError(Exception):
    pass


def get_weather(city):
    # Hämtar koordinaterna för den valda staden
    if city not in CITIES:
        raise ValueError("Ogiltig stad")

    latitude, longitude = CITIES[city]

    # Väljer vilken väderdata API:et ska returnera
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 3,
    }

    # Hämtar väderdata och hanterar eventuella anslutningsfel
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        raise WeatherAPIError(
            "Kunde inte hämta väderdata. Försök igen senare."
        ) from error
