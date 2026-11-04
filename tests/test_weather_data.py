from weather_data import format_forecast


# Testar att väderdata omvandlas till rätt format
def test_format_forecast():

    # Skapar exempeldata som liknar svaret från väder-API:et
    data = {
        "daily": {
            "time": ["2026-11-04"],
            "temperature_2m_max": [10.4],
            "temperature_2m_min": [6.0],
            "precipitation_sum": [0.0],
        }
    }

    # Anropar funktionen med vår testdata
    result = format_forecast(data)

    # Kontrollerar att resultatet innehåller en prognosdag
    assert len(result) == 1

    # Kontrollerar att datum, temperatur och nederbörd stämmer
    assert result[0]["date"] == "2026-11-04"
    assert result[0]["max_temp"] == 10.4
    assert result[0]["min_temp"] == 6.0
    assert result[0]["precipitation"] == 0.0
