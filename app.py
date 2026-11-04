from flask import Flask, render_template, request

from cities import CITIES, is_valid_city
from weather_api import WeatherAPIError, get_weather
from weather_data import format_forecast

# Skapar Flask-applikationen
app = Flask(__name__)


# Formaterar temperaturer med svenskt decimaltecken
@app.template_filter("format_temp")
def format_temp(value):
    return f"{float(value):.1f}".replace(".", ",") + " °C"


# Startsidan med formulär för att välja stad
@app.route("/")
def home():
    return render_template(
        "index.html",
        cities=CITIES,
    )


# Visar aktuell väderinformation och tredagarsprognos
@app.route("/forecast")
def forecast():
    # Hämtar vald stad från URL:en
    city = request.args.get("city", "Stockholm")

    # Kontrollerar att staden finns i listan
    if not is_valid_city(city):
        return render_template(
            "forecast.html",
            selected_city=city,
            current_weather=None,
            forecast=[],
            error="Staden finns inte i listan.",
        ), 400

    # Hämtar och bearbetar väderdata från API:et
    try:
        weather = get_weather(city)
        current_weather = weather["current"]
        daily_forecast = format_forecast(weather)

    # Hanterar fel om API:et inte svarar
    except WeatherAPIError as error:
        print(f"Fel vid hämtning av väderdata: {error}")
        return render_template(
            "forecast.html",
            selected_city=city,
            current_weather=None,
            forecast=[],
            error="Kunde inte hämta väderdata just nu.",
        ), 503

    # Skickar väderinformationen till prognossidan
    return render_template(
        "forecast.html",
        selected_city=city,
        current_weather=current_weather,
        forecast=daily_forecast,
        error=None,
    )


# Visar en egen felsida om adressen inte finns
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# Startar Flask-servern lokalt
if __name__ == "__main__":
    app.run(debug=True, port=5001)
