from flask import Flask, render_template, request

from cities import CITIES, is_valid_city
from weather_api import WeatherAPIError, get_weather
from weather_data import format_forecast, get_weather_icon

# Skapar Flask-applikationen
app = Flask(__name__)


# Eget Jinja-filter som visar temperatur med svenskt decimaltecken
@app.template_filter("format_temp")
def format_temp(value):
    return f"{float(value):.1f}".replace(".", ",") + " °C"


# Gör väderikonerna tillgängliga i HTML-mallarna
app.jinja_env.globals["get_weather_icon"] = get_weather_icon


# Startsidan där användaren kan välja stad
@app.route("/")
def home():
    return render_template("index.html", cities=CITIES)


# Hämtar och visar väderprognosen för vald stad
@app.route("/forecast")
def forecast():
    # Läser staden från URL:en, Stockholm används som standard
    city = request.args.get("city", "Stockholm")

    # Kontrollerar att staden finns i vår lista
    if not is_valid_city(city):
        return (
            render_template(
                "forecast.html",
                selected_city=city,
                current_weather=None,
                forecast=[],
                error="Staden finns inte i listan.",
            ),
            400,
        )

    try:
        # Hämtar väderdata från Open-Meteo
        weather = get_weather(city)

        # Hämtar aktuellt väder och formaterar tredagarsprognosen
        current_weather = weather["current"]
        daily_forecast = format_forecast(weather)

    except WeatherAPIError as error:
        # Hanterar fel om API:et inte svarar
        print(f"Fel vid hämtning av väderdata: {error}")

        return (
            render_template(
                "forecast.html",
                selected_city=city,
                current_weather=None,
                forecast=[],
                error="Kunde inte hämta väderdata just nu.",
            ),
            503,
        )

    # Skickar väderinformationen till HTML-mallen
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


# Startar Flask lokalt på port 5001
if __name__ == "__main__":
    app.run(debug=True, port=5001)
