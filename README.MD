# Weather Dashboard

En väderapplikation byggd med Python och Flask som visar aktuellt väder och en tredagarsprognos för fem svenska städer.

Projektet är en individuell examinationsuppgift i Programmering 2.

## Funktioner

- Välj mellan Stockholm, Göteborg, Malmö, Umeå och Kiruna.
- Visa aktuell temperatur och vindhastighet.
- Visa tredagarsprognos med max- och mintemperatur samt nederbörd.
- Visa prognosen i både väderkort och tabell.
- Hantera ogiltiga städer och API-fel.
- Visa en egen 404-sida.
- Formatera temperaturer med ett eget Jinja2-filter.

## Tekniker

- Python
- Flask och Jinja2
- Requests
- Pytest och unittest.mock
- Ruff
- HTML och CSS

## Installation

Klona projektet från GitHub och öppna projektmappen.

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

```bash
python app.py
```

Öppna sedan:

http://127.0.0.1:5001

## Kör testerna

```bash
python -m pytest -v
```

Kontrollera kodkvalitet och formatering:

```bash
ruff check .
ruff format --check .
```

## Frågor och svar

### Varför använder vi mock i API-tester?

Mock används för att simulera API-svar utan att göra riktiga nätverksanrop. Det gör testerna snabbare och mer pålitliga. Vi kan även simulera fel som timeout och HTTP-fel.

### Varför använder vi timeout och raise_for_status()?

Timeout förhindrar att applikationen väntar hur länge som helst på ett API-svar. `raise_for_status()` gör att HTTP-fel upptäcks och kan hanteras med ett tydligt felmeddelande.

### Varför använder vi mallarv i Jinja2?

Mallarv gör att flera HTML-sidor kan dela samma grundstruktur genom `base.html`. Det minskar upprepning och gör koden enklare att underhålla.

### Varför använder vi en fixture i pytest?

En fixture skapar gemensamma resurser som flera tester kan använda. I projektet använder vi en Flask-testklient för att testa olika routes utan att starta en riktig webbserver.

## Datakälla

Väderdata hämtas från [Open-Meteo](https://open-meteo.com/).

Data: Open-Meteo, tillgänglig enligt CC BY 4.0. Se [Open-Meteos dokumentation](https://open-meteo.com/en/docs).