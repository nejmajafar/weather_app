import requests

# API-adress för att hämta väderdata
url = "https://api.open-meteo.com/v1/forecast"

# Väljer Stockholm och vilken väderinformation vi vill hämta
params = {
    "latitude": 59.33,
    "longitude": 18.07,
    "current": "temperature_2m,wind_speed_10m",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "auto",
    "forecast_days": 3,
}

# Skickar en förfrågan till API:et
response = requests.get(url, params=params, timeout=10)
response.raise_for_status()

# Omvandlar JSON-svaret till Python-data
data = response.json()

print(data)
