import math


def validate_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("Аргумент должен быть числом")
    if not math.isfinite(value):
        raise ValueError("Аргумент должен быть конечным числом")
    return value


def add(a, b):
    return validate_number(a) + validate_number(b)


def subtract(a, b):
    return validate_number(a) - validate_number(b)


def multiply(a, b):
    return validate_number(a) * validate_number(b)


def divide(a, b):
    a = validate_number(a)
    b = validate_number(b)
    if b == 0:
        raise ZeroDivisionError("Деление на ноль запрещено")
    return a / b


def classify_number(x):
    x = validate_number(x)
    if x > 0:
        return "positive"
    elif x == 0:
        return "zero"
    else:
        return "negative"


def calculate(operation, a, b):
    if operation == "+":
        return add(a, b)
    elif operation == "-":
        return subtract(a, b)
    elif operation == "*":
        return multiply(a, b)
    elif operation == "/":
        return divide(a, b)
    else:
        raise ValueError("Неизвестная операция")
