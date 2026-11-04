# Lagrar städer och deras geografiska koordinater
# Varje stad har en latitud och longitud
CITIES = {
    "Stockholm": (59.33, 18.07),
    "Göteborg": (57.71, 11.97),
    "Malmö": (55.61, 13.00),
    "Umeå": (63.83, 20.26),
    "Kiruna": (67.86, 20.23),
}


def is_valid_city(city):
    # Kontrollerar om den valda staden finns i CITIES
    # Returnerar True om staden finns, annars False
    return city in CITIES
