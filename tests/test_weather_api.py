from unittest.mock import Mock, patch

import pytest
import requests

from weather_api import WeatherAPIError, get_weather


# Testar att väderdata hämtas korrekt från API:et
def test_get_weather_success():
    mock_response = Mock()
    mock_response.json.return_value = {"current": {"temperature_2m": 10.4}}

    # Ersätter det riktiga API-anropet med testdata
    with patch("weather_api.requests.get", return_value=mock_response) as mock_get:
        result = get_weather("Stockholm")

    assert result["current"]["temperature_2m"] == 10.4
    mock_get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()


# Testar att ett timeout-fel hanteras korrekt
def test_get_weather_timeout():
    with (
        patch("weather_api.requests.get", side_effect=requests.Timeout),
        pytest.raises(WeatherAPIError),
    ):
        get_weather("Stockholm")


# Testar att ett HTTP-fel hanteras korrekt
def test_get_weather_http_error():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("Serverfel")

    # Simulerar ett misslyckat API-anrop
    with (
        patch("weather_api.requests.get", return_value=mock_response),
        pytest.raises(WeatherAPIError),
    ):
        get_weather("Stockholm")
