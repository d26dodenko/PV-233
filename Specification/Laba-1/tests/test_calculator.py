"""Позитивные, негативные и граничные проверки по контракту калькулятора."""

import math

import pytest

from calculator import calculate


@pytest.mark.parametrize(
    "left,operator,right,expected",
    [
        (2, "+", 3, 5),
        (-2, "-", 3, -5),
        (-2, "*", -3, 6),
        (5, "/", 2, 2.5),
        (0, "*", 8, 0),
        (0.1, "+", 0.2, 0.3),
        (1e100, "/", 1e100, 1),
        (0, "/", -2, 0),
    ],
)
def test_arithmetic(left, operator, right, expected):
    assert calculate(left, operator, right) == pytest.approx(expected)


@pytest.mark.parametrize("value", [True, False, "1", None, [], {}])
@pytest.mark.parametrize("side", ["left", "right"])
def test_invalid_types(value, side):
    with pytest.raises(TypeError, match="operands must be real numbers"):
        calculate(value if side == "left" else 1, "+", value if side == "right" else 1)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
@pytest.mark.parametrize("side", ["left", "right"])
def test_non_finite(value, side):
    with pytest.raises(ValueError, match="operands must be finite"):
        calculate(value if side == "left" else 1, "+", value if side == "right" else 1)


@pytest.mark.parametrize("zero", [0, 0.0, -0.0])
def test_division_by_zero(zero):
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        calculate(1, "/", zero)


@pytest.mark.parametrize("operator", ["**", "", None])
def test_unsupported_operation(operator):
    with pytest.raises(ValueError, match="unsupported operator"):
        calculate(1, operator, 2)


def test_overflow():
    with pytest.raises(OverflowError, match="result must be finite"):
        calculate(1e308, "*", 2)
