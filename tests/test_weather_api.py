from unittest.mock import patch, Mock

import pytest
import requests

from weather_api import get_weather, WeatherAPIError


# Testar att API:et returnerar väderdata
@patch("weather_api.requests.get")
def test_get_weather_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "current": {"temperature_2m": 10}
    }
    mock_get.return_value = mock_response

    result = get_weather("Stockholm")

    assert result["current"]["temperature_2m"] == 10


# Testar att ett timeout-fel hanteras
@patch("weather_api.requests.get")
def test_get_weather_timeout(mock_get):
    mock_get.side_effect = requests.Timeout()

    with pytest.raises(WeatherAPIError):
        get_weather("Stockholm")


# Testar att ett HTTP-fel hanteras
@patch("weather_api.requests.get")
def test_get_weather_http_error(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError()
    mock_get.return_value = mock_response

    with pytest.raises(WeatherAPIError):
        get_weather("Stockholm")