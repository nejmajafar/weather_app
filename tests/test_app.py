from unittest.mock import patch

import pytest

from app import app


# Skapar en testklient som kan anropa Flask utan webbläsare
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


# Kontrollerar att startsidan fungerar
def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Stockholm" in response.get_data(as_text=True)


# Kontrollerar att väderprognosen visas med testdata
def test_forecast_success(client):
    mock_weather = {
        "current": {
            "temperature_2m": 7.2,
            "wind_speed_10m": 15.8,
            "weather_code": 3,
        },
        "daily": {
            "time": ["2026-11-04", "2026-11-05", "2026-11-06"],
            "temperature_2m_max": [10.4, 9.3, 6.6],
            "temperature_2m_min": [6.0, 4.6, 3.0],
            "precipitation_sum": [0.0, 0.0, 0.0],
            "weather_code": [3, 1, 61],
        },
    }

    # Ersätter det riktiga API-anropet med testdata
    with patch("app.get_weather", return_value=mock_weather):
        response = client.get("/forecast?city=Stockholm")

    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Stockholm" in page
    assert "7,2 °C" in page
    assert "Onsdag 4 november" in page


# Kontrollerar att en ogiltig stad ger felkod 400
def test_invalid_city(client):
    response = client.get("/forecast?city=Paris")

    assert response.status_code == 400
    assert "Staden finns inte i listan." in response.get_data(as_text=True)


# Kontrollerar att en okänd adress visar vår 404-sida
def test_page_not_found(client):
    response = client.get("/finns-inte")

    assert response.status_code == 404


# Kontrollerar felhanteringen om väder-API:et inte fungerar
def test_forecast_api_error(client):
    from weather_api import WeatherAPIError

    with patch(
        "app.get_weather",
        side_effect=WeatherAPIError("API-fel"),
    ):
        response = client.get("/forecast?city=Stockholm")

    assert response.status_code == 503
    assert "Kunde inte hämta väderdata just nu." in response.get_data(as_text=True)
