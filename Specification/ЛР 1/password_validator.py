import re

MIN_LENGTH = 8

def validate_password(password: str) -> dict:
    """Проверяет пароль и возвращает словарь с результатами."""
    errors = []

    if len(password) < MIN_LENGTH:
        errors.append("too_short")
    if not re.search(r"[A-Z]", password):
        errors.append("no_uppercase")
    if not re.search(r"[a-z]", password):
        errors.append("no_lowercase")
    if not re.search(r"\d", password):
        errors.append("no_digit")
    if not re.search(r"[!@#$%^&*]", password):
        errors.append("no_special")

    return {"valid": len(errors) == 0, "errors": errors}


def strength(password: str) -> str:
    """Оценивает надёжность пароля."""
    score = 0
    if len(password) >= MIN_LENGTH: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[!@#$%^&*]", password): score += 1

    if score <= 1:
        return "weak"
    elif score <= 3:
        return "medium"
    else:
        return "strong"