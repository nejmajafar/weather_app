from datetime import date


# Väljer väderikon utifrån väderkoden från Open-Meteo
def get_weather_icon(code):
    if code is None:
        return "🌤️"

    if code == 0:
        return "☀️"

    if code in (1, 2):
        return "🌤️"

    if code == 3:
        return "☁️"

    if code in (45, 48):
        return "🌫️"

    if code in (51, 53, 55, 56, 57):
        return "🌦️"

    if code in (61, 63, 65, 66, 67, 80, 81, 82):
        return "🌧️"

    if code in (71, 73, 75, 77, 85, 86):
        return "❄️"

    if code in (95, 96, 99):
        return "⛈️"

    return "🌤️"


# Omvandlar API:ets datum till ett läsbart svenskt datum
def format_date(date_string):
    months = [
        "januari",
        "februari",
        "mars",
        "april",
        "maj",
        "juni",
        "juli",
        "augusti",
        "september",
        "oktober",
        "november",
        "december",
    ]

    weekdays = [
        "Måndag",
        "Tisdag",
        "Onsdag",
        "Torsdag",
        "Fredag",
        "Lördag",
        "Söndag",
    ]

    # Omvandlar datumtexten till ett Python-datum
    day = date.fromisoformat(date_string)

    return f"{weekdays[day.weekday()]} {day.day} {months[day.month - 1]}"


# Gör om API:ets dagliga väderdata till en lista med dictionaries
def format_forecast(data):
    daily = data["daily"]
    forecast = []

    # Hämtar väderkoderna om de finns i API-svaret
    weather_codes = daily.get("weather_code", [])

    # Går igenom varje dag i prognosen
    for i in range(len(daily["time"])):
        weather_code = weather_codes[i] if i < len(weather_codes) else None

        day = {
            "date": daily["time"][i],
            "display_date": format_date(daily["time"][i]),
            "max_temp": daily["temperature_2m_max"][i],
            "min_temp": daily["temperature_2m_min"][i],
            "precipitation": daily["precipitation_sum"][i],
            "weather_icon": get_weather_icon(weather_code),
        }

        forecast.append(day)

    # Returnerar den färdiga prognosen till Flask
    return forecast
