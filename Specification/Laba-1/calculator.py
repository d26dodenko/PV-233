"""Калькулятор для работы по метрикам качества; контракт ограничен конечными числами."""

import math


def calculate(left: float, operator: str, right: float) -> float:
    """Вычислить +, -, *, /; отклонить bool, неверные типы, NaN и переполнение."""
    for value in (left, right):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("operands must be real numbers, not bool")
        if not math.isfinite(value):
            raise ValueError("operands must be finite")
    if operator == "+":
        result = left + right
    elif operator == "-":
        result = left - right
    elif operator == "*":
        result = left * right
    elif operator == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        result = left / right
    else:
        raise ValueError("unsupported operator")
    if not math.isfinite(result):
        raise OverflowError("result must be finite")
    return float(result)
