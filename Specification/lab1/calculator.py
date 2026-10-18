def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Деление на ноль")
    return a / b


def power(a, b):
    return a ** b


def calculate(a, op, b):
    if op == "+":
        return add(a, b)
    elif op == "-":
        return subtract(a, b)
    elif op == "*":
        return multiply(a, b)
    elif op == "/":
        return divide(a, b)
    elif op == "**":
        return power(a, b)
    else:
        raise ValueError(f"Неизвестная операция: {op}")


def classify_number(x):
    if x > 0:
        return "Positive"
    elif x == 0:
        return "Zero"
    else:
        return "Negative"
