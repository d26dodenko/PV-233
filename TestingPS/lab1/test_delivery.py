"""Тест-кейсы лабораторной работы 1. Ожидания заданы независимо от кода."""

import re

import pytest

from delivery import calculate_delivery_cost


@pytest.mark.parametrize(
    "order_amount,distance_km,is_premium,expected",
    [
        pytest.param(1000, 3, False, 200.0, id="TC01-short"),
        pytest.param(1000, 10, False, 500.0, id="TC02-middle"),
        pytest.param(1000, 30, False, 800.0, id="TC03-long"),
        pytest.param(1000, 3, True, 100.0, id="TC04-premium-short"),
        pytest.param(1000, 10, True, 250.0, id="TC05-premium-middle"),
        pytest.param(1000, 30, True, 400.0, id="TC06-premium-long"),
        pytest.param(4999.99, 10, False, 500.0, id="TC07-below-free"),
        pytest.param(5000, 10, False, 0.0, id="TC08-free-threshold"),
        pytest.param(5000.01, 30, False, 0.0, id="TC09-above-free"),
        pytest.param(5000, 10, True, 0.0, id="TC10-free-premium"),
        pytest.param(0, 10, False, 500.0, id="TC11-zero-amount"),
        pytest.param(1000, 0, False, 200.0, id="TC12-zero-distance"),
        pytest.param(1000, 4.99, False, 200.0, id="TC13-below-5"),
        pytest.param(1000, 5, False, 200.0, id="TC14-at-5"),
        pytest.param(1000, 5.01, False, 500.0, id="TC15-above-5"),
        pytest.param(1000, 19.99, False, 500.0, id="TC16-below-20"),
        pytest.param(1000, 20, False, 500.0, id="TC17-at-20"),
        pytest.param(1000, 20.01, False, 500.3, id="TC18-above-20"),
        pytest.param(1000, 20.5, True, 257.5, id="TC19-fractional-premium"),
        pytest.param(0, 0, True, 100.0, id="TC20-both-zero-premium"),
        pytest.param(5000, 0, False, 0.0, id="TC21-free-short"),
        pytest.param(5000, 30, True, 0.0, id="TC22-free-long-premium"),
        pytest.param(4999.99, 10, True, 250.0, id="TC23-paid-premium"),
        pytest.param(1000, 5, True, 100.0, id="TC24-at-5-premium"),
    ],
)
def test_delivery_cost(order_amount, distance_km, is_premium, expected):
    actual = calculate_delivery_cost(order_amount, distance_km, is_premium)
    assert actual == pytest.approx(expected, rel=0, abs=1e-9)
    assert isinstance(actual, float)


@pytest.mark.parametrize(
    "order_amount,distance_km,is_premium,message",
    [
        pytest.param(-1, 10, False, "order_amount must be >= 0", id="TC25-negative-amount"),
        pytest.param(-0.01, 10, True, "order_amount must be >= 0", id="TC26-near-zero-amount"),
        pytest.param(1000, -1, False, "distance_km must be >= 0", id="TC27-negative-distance"),
        pytest.param(1000, -0.01, True, "distance_km must be >= 0", id="TC28-near-zero-distance"),
        pytest.param(5000, -1, True, "distance_km must be >= 0", id="TC29-free-invalid-distance"),
        pytest.param(-1, -1, False, "order_amount must be >= 0", id="TC30-both-negative"),
    ],
)
def test_invalid_inputs(order_amount, distance_km, is_premium, message):
    with pytest.raises(ValueError, match="^" + re.escape(message) + "$"):
        calculate_delivery_cost(order_amount, distance_km, is_premium)
