def calculate_ride_cost(minutes: float, bonus_points: int, is_premium: bool) -> float:
    """
    Расчёт стоимости поездки в каршеринге.

    Бизнес-правила:
    1. Если minutes < 0 или bonus_points < 0 — ValueError.
    2. Если bonus_points >= 1000 — поездка полностью оплачивается бонусами (0).
    3. Иначе:
       - minutes <= 30: 150 (пакет «30 минут»)
       - 30 < minutes <= 120: 400 (пакет «2 часа»)
       - minutes > 120: 400 + (minutes - 120) * 3
    4. Для is_premium=True применяется скидка 30% на стоимость поездки.
    """
    if minutes < 0:
        raise ValueError("minutes must be >= 0")
    if bonus_points < 0:
        raise ValueError("bonus_points must be >= 0")

    if bonus_points >= 1000:
        cost = 0.0
    elif minutes <= 30:
        cost = 150.0
    elif minutes <= 120:
        cost = 400.0
    else:
        cost = 400.0 + (minutes - 120) * 3.0

    if is_premium:
        cost *= 0.7

    return cost