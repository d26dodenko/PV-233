import math

import pytest

from calculator import (
    add,
    calculate,
    classify_number,
    divide,
    multiply,
    subtract,
    validate_number,
)


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5), (-2, 3, 1), (0, 0, 0), (0.1, 0.2, 0.3),
])
def test_add(a, b, expected):
    assert add(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a,b,expected", [(5, 2, 3), (2, 5, -3), (-2, -3, 1)])
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [(4, 3, 12), (-4, 3, -12), (9, 0, 0)])
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [(8, 2, 4), (-9, 3, -3), (3, 2, 1.5)])
def test_divide(a, b, expected):
    assert divide(a, b) == expected


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
        divide(10, 0)


@pytest.mark.parametrize("number,label", [(7, "positive"), (0, "zero"), (-7, "negative")])
def test_classify_number(number, label):
    assert classify_number(number) == label


@pytest.mark.parametrize("op,a,b,expected", [
    ("+", 2, 3, 5), ("-", 2, 3, -1), ("*", 2, 3, 6), ("/", 6, 3, 2),
])
def test_calculate(op, a, b, expected):
    assert calculate(op, a, b) == expected


def test_unknown_operation():
    with pytest.raises(ValueError, match="Неизвестная операция"):
        calculate("^", 2, 3)


@pytest.mark.parametrize("value", ["4", None, True, False, [1]])
def test_non_numeric_type(value):
    with pytest.raises(TypeError, match="должен быть числом"):
        validate_number(value)


@pytest.mark.parametrize("value", [math.inf, -math.inf, math.nan])
def test_non_finite_number(value):
    with pytest.raises(ValueError, match="конечным"):
        validate_number(value)


def test_valid_integer():
    assert validate_number(7) == 7


def test_valid_float():
    assert validate_number(3.5) == 3.5


def test_divide_validates_both_operands():
    with pytest.raises(TypeError):
        divide("10", 2)
    with pytest.raises(TypeError):
        divide(10, "2")
