import pytest
from delivery import calculate_delivery_cost

# shot function name
def cost(amount, distance, premium):
    return calculate_delivery_cost(amount, distance, premium)


# ---------- Позитивные ----------
def test_tc01_short_distance():
    assert cost(1000, 2, False) == pytest.approx(150.0)


def test_tc02_middle_distance():
    assert cost(1000, 10, False) == pytest.approx(400.0)


def test_tc03_long_distance():
    assert cost(1000, 25, False) == pytest.approx(650.0)


# ---------- Негативные ----------
def test_tc04_negative_order_amount():
    with pytest.raises(ValueError, match="order_amount"):
        cost(-1, 10, False) 


def test_tc05_negative_distance_km():
    with pytest.raises(ValueError, match="distance_km"):
        cost(100, -10, False) 


def test_tc06_negative_both():
    with pytest.raises(ValueError, match="order_amount"):
        cost(-1, -10, False) 


# ---------- Граничные ----------
def test_tc07_distance_km_zero():
    assert cost(1000, 0, False) == pytest.approx(150.0)


def test_tc08_distance_exactly_3():
    assert cost(1000, 3, False) == pytest.approx(150.0)


def test_tc09_distance_just_above_3():
    assert cost(1000, 3.01, False) == pytest.approx(400.0)
 
 
def test_tc10_distance_exactly_15():
    assert cost(1000, 15, False) == pytest.approx(400.0)
 
 
def test_tc11_distance_just_above_15():
    assert cost(1000, 16, False) == pytest.approx(425.0)


# ----------  Premium-пользователь ----------
def test_tc12_with_premium():
    assert cost(1000, 10, True) == pytest.approx(280.0)


def test_tc13_with_premium_short_distance():
    assert cost(2000, 2, True) == pytest.approx(105.0)

# ----------  Free-delivery ----------
def test_tc14_free_delivery_exactly_3000():
    assert cost(3000, 10, False) == 0.0


def test_tc15_paid_delivery_just_below_3000():
    assert cost(2999.99, 10, False) == pytest.approx(400.0)


def test_tc16_free_delivery_far_distance():
    assert cost(10000, 100, False) == 0.0
 
 
def test_tc17_order_amount_zero():
    assert cost(0, 10, False) == pytest.approx(400.0)
