import pytest

from main import calculate_order_total


def test_zero_items_and_zero_distance():
    assert calculate_order_total(0, 0, False) == pytest.approx(150.0)


def test_min_positive_items_short_distance():
    assert calculate_order_total(0.01, 3, False) == pytest.approx(150.01)


def test_distance_boundary_3_km():
    assert calculate_order_total(1000, 3, False) == pytest.approx(1150.0)


def test_just_over_3_km():
    assert calculate_order_total(1000, 3.01, False) == pytest.approx(1300.0)


def test_distance_boundary_10_km():
    assert calculate_order_total(1000, 10, False) == pytest.approx(1300.0)


def test_just_over_10_km():
    assert calculate_order_total(1000, 10.01, False) == pytest.approx(1300.25)


def test_long_distance_20_km():
    assert calculate_order_total(1000, 20, False) == pytest.approx(1550.0)


def test_items_below_free_threshold_2999_99():
    assert calculate_order_total(2999.99, 10, False) == pytest.approx(3299.99)


def test_free_delivery_at_3000():
    assert calculate_order_total(3000, 10, False) == pytest.approx(3000.0)


def test_free_delivery_above_3000_long_distance():
    assert calculate_order_total(5000, 50, False) == pytest.approx(5000.0)


def test_premium_discount_middle_distance():
    assert calculate_order_total(1000, 10, True) == pytest.approx(1240.0)


def test_premium_discount_long_distance():
    assert calculate_order_total(1000, 20, True) == pytest.approx(1440.0)


def test_premium_free_delivery():
    assert calculate_order_total(3000, 20, True) == pytest.approx(3000.0)


def test_negative_items_total():
    with pytest.raises(ValueError, match="items_total must be >= 0"):
        calculate_order_total(-1, 10, False)


def test_negative_distance():
    with pytest.raises(ValueError, match="distance_km must be >= 0"):
        calculate_order_total(1000, -1, False)