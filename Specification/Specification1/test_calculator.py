import math

import pytest

from calculator import (
    add,
    calculate,
    divide,
    multiply,
    percent,
    power,
    square_root,
    subtract,
)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (-2, -3, -5),
        (0, 0, 0),
        (1.5, 2.5, 4.0),
    ],
    ids=["positive", "negative", "zeros", "floats"],
)
def test_add(a, b, expected):
    assert add(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2),
        (3, 5, -2),
        (0, 0, 0),
        (1.5, 0.5, 1.0),
    ],
    ids=["positive_result", "negative_result", "zeros", "floats"],
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),
        (-2, 3, -6),
        (0, 100, 0),
        (1.5, 2, 3.0),
    ],
    ids=["positive", "negative", "zero", "floats"],
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 2, 3.0),
        (-6, 2, -3.0),
        (0, 5, 0.0),
        (1, 4, 0.25),
    ],
    ids=["positive", "negative", "zero_dividend", "fraction"],
)
def test_divide(a, b, expected):
    assert divide(a, b) == pytest.approx(expected)


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 8),
        (2, 0, 1),
        (9, 0.5, 3.0),
        (-2, 3, -8),
    ],
    ids=["positive", "zero_exponent", "fractional", "negative_base"],
)
def test_power(a, b, expected):
    assert power(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, expected",
    [
        (9, 3.0),
        (0, 0.0),
        (2, math.sqrt(2)),
    ],
    ids=["perfect_square", "zero", "irrational"],
)
def test_square_root(a, expected):
    assert square_root(a) == pytest.approx(expected)


def test_square_root_negative():
    with pytest.raises(ValueError):
        square_root(-1)


@pytest.mark.parametrize(
    "value, percent_value, expected",
    [
        (200, 10, 20.0),
        (100, 0, 0.0),
        (50, 50, 25.0),
    ],
    ids=["ten_percent", "zero_percent", "half"],
)
def test_percent(value, percent_value, expected):
    assert percent(value, percent_value) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b, operation, expected",
    [
        (2, 3, "add", 5),
        (5, 3, "subtract", 2),
        (2, 3, "multiply", 6),
        (6, 2, "divide", 3.0),
        (2, 3, "power", 8),
        (200, 10, "percent", 20.0),
    ],
    ids=["add", "subtract", "multiply", "divide", "power", "percent"],
)
def test_calculate_dispatch(a, b, operation, expected):
    assert calculate(a, b, operation) == pytest.approx(expected)


def test_calculate_unknown_operation():
    with pytest.raises(ValueError):
        calculate(1, 2, "mod")