import pytest

from cities import is_valid_city


# Testar flera giltiga städer med samma testfunktion
@pytest.mark.parametrize(
    "city",
    ["Stockholm", "Göteborg", "Malmö", "Umeå", "Kiruna"],
)
def test_valid_city(city):
    assert is_valid_city(city) is True


# Testar flera ogiltiga städer
@pytest.mark.parametrize(
    "city",
    ["Paris", "London", "Berlin", ""],
)
def test_invalid_city(city):
    assert is_valid_city(city) is False
