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
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 3,
    }

    # Skickar en GET-förfrågan till väder-API:et
    try:
        response = requests.get(API_URL, params=params, timeout=10)

        # Kontrollerar om API-anropet lyckades
        response.raise_for_status()

        # Omvandlar JSON-svaret till Python-data
        return response.json()

    # Hanterar fel vid anslutning eller API-anrop
    except requests.RequestException as error:
        raise WeatherAPIError(
            "Kunde inte hämta väderdata. Försök igen senare."
        ) from error
