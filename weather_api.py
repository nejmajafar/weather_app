import requests

from cities import CITIES

# Adressen till Open-Meteos väder-API
API_URL = "https://api.open-meteo.com/v1/forecast"


# Eget fel som används när väderdata inte kan hämtas
class WeatherAPIError(Exception):
    pass


def get_weather(city):
    # Kontrollerar att staden finns i vår dictionary
    if city not in CITIES:
        raise ValueError("Ogiltig stad")

    # Hämtar stadens latitud och longitud
    latitude, longitude = CITIES[city]

    # Anger vilken väderdata API:et ska returnera
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "daily": (
            "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code"
        ),
        "timezone": "auto",
        "forecast_days": 3,
    }

    try:
        # Skickar API-anropet och väntar högst 10 sekunder
        response = requests.get(API_URL, params=params, timeout=10)

        # Kontrollerar om servern har returnerat ett HTTP-fel
        response.raise_for_status()

        # Omvandlar JSON-svaret till Python-data
        return response.json()

    except requests.RequestException as error:
        # Hanterar exempelvis timeout och anslutningsfel
        raise WeatherAPIError(
            "Kunde inte hämta väderdata. Försök igen senare."
        ) from error
