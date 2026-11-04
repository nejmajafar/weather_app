def format_forecast(data):
    # Hämtar den dagliga prognosen från API-svaret
    daily = data["daily"]

    # Skapar en tom lista för väderprognosen
    forecast = []

    # Går igenom varje dag i prognosen
    for i in range(len(daily["time"])):
        # Samlar väderinformationen för en dag
        day = {
            "date": daily["time"][i],
            "max_temp": daily["temperature_2m_max"][i],
            "min_temp": daily["temperature_2m_min"][i],
            "precipitation": daily["precipitation_sum"][i],
        }

        # Lägger till dagens väder i listan
        forecast.append(day)

    # Returnerar den färdiga väderprognosen
    return forecast
