# Weather Dashboard

En väderapplikation byggd med Python och Flask som visar aktuellt väder och en tredagarsprognos för fem svenska städer.

Projektet är en individuell examinationsuppgift i Programmering 2.

## Funktioner

- Välj mellan Stockholm, Göteborg, Malmö, Umeå och Kiruna.
- Visa aktuell temperatur och vindhastighet.
- Visa en tredagarsprognos med högsta och lägsta temperatur samt nederbörd.
- Visa väderinformation med väderikoner, prognoskort och en detaljerad tabell.
- Hantera ogiltiga städer och fel vid API-anrop.
- Visa en egen 404-sida.
- Formatera temperaturer med ett eget Jinja2-filter.
- Visa datum på svenska.

## Tekniker

- Python
- Flask och Jinja2
- Requests
- Pytest och unittest.mock
- Ruff
- HTML och CSS

## Installation

Klona projektet från GitHub:

```bash
git clone https://github.com/nejmajafar/weather_app.git
```

Öppna projektmappen:

```bash
cd weather_app
```

Skapa en virtuell miljö:

```bash
python -m venv venv
```

Aktivera den på macOS:

```bash
source venv/bin/activate
```

Installera beroenden:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Starta applikationen

Starta Flask-applikationen:

```bash
python app.py
```

Öppna sedan följande adress i webbläsaren:

http://127.0.0.1:5001

Välj en stad på startsidan och klicka på knappen för att visa väderprognosen.

## Kör testerna

Projektet använder Pytest för att testa funktioner, API-anrop och Flask-routes.

Kör testerna:

```bash
python -m pytest -v
```

Kontrollera kodkvaliteten:

```bash
ruff check .
```

Kontrollera formateringen:

```bash
ruff format --check .
```

Tester som använder API-data körs med mockning för att inte vara beroende av internetuppkoppling.

## Frågor och svar

### 1. Varför mockar du anropen mot API:et i dina tester, och vad skulle hända om du inte gjorde det?

Jag använder mockning för att simulera svar från Open-Meteo utan att göra riktiga API-anrop. Det gör testerna snabbare och mer pålitliga eftersom de inte är beroende av internet eller att API:et fungerar. Utan mockning skulle testerna kunna misslyckas på grund av nätverksproblem även om min egen kod fungerar. I `tests/test_weather_api.py` testar jag både lyckade anrop och fel som timeout och HTTP-fel.

### 2. Vad gör timeout och raise_for_status(), och varför behövs de?

I `weather_api.py` använder jag `timeout=10` för att begränsa hur länge programmet väntar på ett svar från API:et. `raise_for_status()` kontrollerar HTTP-statuskoden och skapar ett undantag om servern returnerar ett fel, exempelvis 404 eller 500. Felen fångas med `requests.RequestException` och omvandlas till mitt eget fel `WeatherAPIError`. På så sätt kan applikationen visa ett tydligt felmeddelande i stället för att krascha.

### 3. Hur fungerar mallarv i Jinja2? Förklara med exempel från dina egna mallar.

Mallarv innebär att flera HTML-sidor kan använda samma grundstruktur utan att koden behöver upprepas. I mitt projekt innehåller `base.html` gemensamma delar som navigation, sidhuvud och sidfot. Mallarna `index.html` och `forecast.html` använder `{% extends "base.html" %}` och lägger sitt eget innehåll i blocket `content`. Det gör det enklare att ändra designen eftersom gemensamma delar bara behöver uppdateras på ett ställe.

### 4. Vad är en fixture, och vilken använder du?

En fixture i Pytest används för att förbereda resurser som behövs i flera tester. I `tests/test_app.py` använder jag `@pytest.fixture` för att skapa en Flask-testklient. Med testklienten kan jag skicka förfrågningar till mina routes och kontrollera statuskoder och sidinnehåll utan att starta en riktig webbserver. Det gör testerna enklare att skriva och återanvända.

## Projektstruktur

- `app.py` – Flask-applikationen med routes och felhantering.
- `cities.py` – Lista över städer och deras koordinater samt validering.
- `weather_api.py` – API-anrop till Open-Meteo.
- `weather_data.py` – Formatering av prognosdata, datum och väderikoner.
- `templates/` – HTML-mallar för startsida, prognos och felsida.
- `static/style.css` – Webbplatsens design och layout.
- `tests/` – Automatiserade tester med Pytest.
- `requirements.txt` – Applikationens beroenden.
- `requirements-dev.txt` – Verktyg för tester och kodkontroll.
- `pyproject.toml` – Projektets konfiguration för tester och kodverktyg.

## Datakälla

Väderdata hämtas från [Open-Meteo](https://open-meteo.com/), som tillhandahåller väderprognoser via ett öppet API.

Data från Open-Meteo används enligt CC BY 4.0.

Dokumentation: [Open-Meteo Weather Forecast API](https://open-meteo.com/en/docs)