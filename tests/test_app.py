from unittest.mock import patch

import pytest

from app import app
from weather_api import WeatherAPIError


# Skapar en testklient för Flask
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


# Testar att startsidan fungerar
def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Weather Dashboard" in response.data


# Testar prognossidan med simulerad väderdata
def test_forecast_success(client):
    mock_weather = {
        "current": {
            "temperature_2m": 7.2,
            "wind_speed_10m": 15.8,
        },
        "daily": {
            "time": ["2026-11-04", "2026-11-05", "2026-11-06"],
            "temperature_2m_max": [10.4, 9.3, 6.6],
            "temperature_2m_min": [6.0, 4.6, 3.0],
            "precipitation_sum": [0.0, 0.0, 0.0],
        },
    }

    # Ersätter API-anropet med testdata
    with patch("app.get_weather", return_value=mock_weather):
        response = client.get("/forecast?city=Stockholm")

    assert response.status_code == 200
    assert "Just nu i Stockholm" in response.get_data(as_text=True)
    assert "10,4 °C" in response.get_data(as_text=True)


# Testar att en ogiltig stad ger HTTP 400
def test_invalid_city(client):
    response = client.get("/forecast?city=Paris")

    assert response.status_code == 400
    assert "Staden finns inte i listan" in response.get_data(as_text=True)


# Testar att en okänd adress ger HTTP 404
def test_page_not_found(client):
    response = client.get("/finns-inte")

    assert response.status_code == 404
    assert "Sidan kunde inte hittas" in response.get_data(as_text=True)


# Testar att ett API-fel hanteras korrekt
def test_forecast_api_error(client):
    with patch(
        "app.get_weather",
        side_effect=WeatherAPIError("API-fel"),
    ):
        response = client.get("/forecast?city=Stockholm")

    assert response.status_code == 503
    assert "Kunde inte hämta väderdata" in response.get_data(as_text=True)
