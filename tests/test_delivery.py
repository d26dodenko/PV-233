"""Тест-кейсы TC-01—TC-34 описаны в docs/report.md."""

import pytest

from delivery import calculate_delivery_cost


@pytest.mark.parametrize(
    "order_amount,distance_km,is_premium,expected",
    [
        pytest.param(0, 0, False, 200.0, id="TC-01-zero"),
        pytest.param(0, 0, True, 100.0, id="TC-02-zero-premium"),
        pytest.param(1000, 2.5, False, 200.0, id="TC-03-short"),
        pytest.param(1000, 2.5, True, 100.0, id="TC-04-short-premium"),
        pytest.param(1000, 4.99, False, 200.0, id="TC-05-before-5"),
        pytest.param(1000, 4.99, True, 100.0, id="TC-06-before-5-premium"),
        pytest.param(1000, 5, False, 200.0, id="TC-07-at-5"),
        pytest.param(1000, 5, True, 100.0, id="TC-08-at-5-premium"),
        pytest.param(1000, 5.01, False, 500.0, id="TC-09-after-5"),
        pytest.param(1000, 5.01, True, 250.0, id="TC-10-after-5-premium"),
        pytest.param(1000, 10, False, 500.0, id="TC-11-middle"),
        pytest.param(1000, 10, True, 250.0, id="TC-12-middle-premium"),
        pytest.param(1000, 19.99, False, 500.0, id="TC-13-before-20"),
        pytest.param(1000, 19.99, True, 250.0, id="TC-14-before-20-premium"),
        pytest.param(1000, 20, False, 500.0, id="TC-15-at-20"),
        pytest.param(1000, 20, True, 250.0, id="TC-16-at-20-premium"),
        pytest.param(1000, 20.01, False, 500.3, id="TC-17-after-20"),
        pytest.param(1000, 20.01, True, 250.15, id="TC-18-after-20-premium"),
        pytest.param(1000, 30, False, 800.0, id="TC-19-long"),
        pytest.param(1000, 30, True, 400.0, id="TC-20-long-premium"),
        pytest.param(4999.99, 10, False, 500.0, id="TC-21-before-5000"),
        pytest.param(4999.99, 10, True, 250.0, id="TC-22-before-5000-premium"),
        pytest.param(5000, 10, False, 0.0, id="TC-23-at-5000"),
        pytest.param(5000, 10, True, 0.0, id="TC-24-at-5000-premium"),
        pytest.param(5000.01, 100, False, 0.0, id="TC-25-after-5000-long"),
        pytest.param(5000.01, 100, True, 0.0, id="TC-26-after-5000-long-premium"),
    ],
)
def test_delivery_cost(order_amount, distance_km, is_premium, expected):
    result = calculate_delivery_cost(order_amount, distance_km, is_premium)

    assert isinstance(result, float)
    assert result == pytest.approx(expected, rel=0, abs=1e-9)


@pytest.mark.parametrize(
    "order_amount,distance_km,is_premium,message",
    [
        pytest.param(-1, 10, False, "order_amount must be >= 0", id="TC-27-negative-order"),
        pytest.param(-0.01, 10, True, "order_amount must be >= 0", id="TC-28-negative-order-premium"),
        pytest.param(1000, -1, False, "distance_km must be >= 0", id="TC-29-negative-distance"),
        pytest.param(1000, -0.01, True, "distance_km must be >= 0", id="TC-30-negative-distance-premium"),
        pytest.param(5000, -1, False, "distance_km must be >= 0", id="TC-31-free-invalid-distance"),
        pytest.param(6000, -1, True, "distance_km must be >= 0", id="TC-32-free-invalid-distance-premium"),
        pytest.param(-1, -1, False, "order_amount must be >= 0", id="TC-33-both-negative"),
        pytest.param(-0.01, 0, True, "order_amount must be >= 0", id="TC-34-negative-order-zero-distance"),
    ],
)
def test_invalid_delivery_input(order_amount, distance_km, is_premium, message):
    with pytest.raises(ValueError) as exc_info:
        calculate_delivery_cost(order_amount, distance_km, is_premium)

    assert str(exc_info.value) == message
