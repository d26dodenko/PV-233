import math


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    return a / b


def power(a: float, b: float) -> float:
    return a ** b


def square_root(a: float) -> float:
    return math.sqrt(a)


def percent(value: float, percent_value: float) -> float:
    return value * percent_value / 100


def calculate(a: float, b: float, operation: str) -> float:
    if operation == "add":
        return add(a, b)
    if operation == "subtract":
        return subtract(a, b)
    if operation == "multiply":
        return multiply(a, b)
    if operation == "divide":
        return divide(a, b)
    if operation == "power":
        return power(a, b)
    if operation == "percent":
        return percent(a, b)
    raise ValueError(f"Unknown operation: {operation}")