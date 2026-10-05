"""Расчёт стоимости доставки по правилам лабораторной работы №1."""


def calculate_delivery_cost(
    order_amount: float, distance_km: float, is_premium: bool
) -> float:
    """Вернуть стоимость доставки; отклонить отрицательную сумму или расстояние.

    От 5000 доставка бесплатна. Иначе тариф составляет 200 до 5 км,
    500 до 20 км и дополнительно 30 за каждый км сверх 20.
    Premium уменьшает стоимость на 50%.
    """
    if order_amount < 0:
        raise ValueError("order_amount must be >= 0")
    if distance_km < 0:
        raise ValueError("distance_km must be >= 0")

    if order_amount >= 5000:
        cost = 0.0
    elif distance_km <= 5:
        cost = 200.0
    elif distance_km <= 20:
        cost = 500.0
    else:
        cost = 500.0 + (distance_km - 20) * 30.0

    if is_premium:
        cost *= 0.5

    return cost
