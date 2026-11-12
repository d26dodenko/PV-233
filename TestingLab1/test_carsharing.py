import pytest
from carsharing import calculate_ride_cost


@pytest.mark.parametrize("minutes, bonus, expected", [
    (10, 0, 150.0),
    (60, 0, 400.0),
    (180, 0, 580.0),
    (1440, 0, 4360.0),
])
def test_positive_tariffs(minutes, bonus, expected):
    assert calculate_ride_cost(minutes, bonus, False) == pytest.approx(expected)

@pytest.mark.parametrize("minutes, expected", [
    (0, 150.0),
    (0.01, 150.0),
    (29.99, 150.0),
    (30, 150.0),
    (30.01, 400.0),
    (119.99, 400.0),
    (120, 400.0),
    (120.01, 400.03),
])
def test_minutes_boundaries(minutes, expected):
    assert calculate_ride_cost(minutes, 0, False) == pytest.approx(expected)

@pytest.mark.parametrize("bonus, expected", [
    (0, 400.0),
    (999, 400.0),
    (1000, 0.0),
    (1001, 0.0),
])
def test_bonus_boundaries(bonus, expected):
    assert calculate_ride_cost(60, bonus, False) == pytest.approx(expected)

def test_free_ride_for_long_trip():
    assert calculate_ride_cost(500, 1000, False) == 0.0

def test_free_ride_with_premium():
    assert calculate_ride_cost(60, 1000, True) == 0.0

@pytest.mark.parametrize("minutes, expected", [
    (10, 105.0),
    (60, 280.0),
    (180, 406.0),
    (120.01, 280.021),
])
def test_premium_discount(minutes, expected):
    assert calculate_ride_cost(minutes, 0, True) == pytest.approx(expected)

@pytest.mark.parametrize("minutes", [-0.01, -1, -1000])
def test_negative_minutes(minutes):
    with pytest.raises(ValueError, match="minutes must be >= 0"):
        calculate_ride_cost(minutes, 0, False)

@pytest.mark.parametrize("bonus", [-1, -0.5])
def test_negative_bonus(bonus):
    with pytest.raises(ValueError, match="bonus_points must be >= 0"):
        calculate_ride_cost(60, bonus, False)

def test_both_negative_first_error_wins():
    with pytest.raises(ValueError, match="minutes must be >= 0"):
        calculate_ride_cost(-1, -1, False)

def test_result_is_float():
    assert isinstance(calculate_ride_cost(10, 0, False), float)
    assert isinstance(calculate_ride_cost(10, 0, True), float)

def test_zero_minutes_uses_min_package():
    assert calculate_ride_cost(0, 0, False) == 150.0