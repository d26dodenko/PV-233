def calculate_loyalty_points(
    rental_days: int,
    car_class: str,
    is_regular_customer: bool,
) -> int:
    """Расчёт бонусных баллов лояльности за аренду автомобиля."""
    if rental_days <= 0:
        raise ValueError("rental_days must be > 0")

    base_rates = {
        "economy": 10,
        "comfort": 20,
        "business": 40,
    }
    if car_class not in base_rates:
        raise ValueError(
            f"car_class must be one of {list(base_rates.keys())}, got {car_class!r}"
        )

    points = base_rates[car_class] * rental_days

    if rental_days <= 3:
        duration_multiplier = 1.0
    elif rental_days <= 7:
        duration_multiplier = 1.1
    elif rental_days <= 29:
        duration_multiplier = 1.25
    else:
        duration_multiplier = 1.5

    points *= duration_multiplier

    if is_regular_customer:
        points *= 1.5

    return round(points)