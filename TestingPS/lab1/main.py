def calculate_order_total(items_total: float, distance_km: float, is_premium: bool) -> float:
    """
    Расчёт итоговой стоимости заказа с учётом доставки.

    Бизнес-правила:
    1. Если items_total < 0 или distance_km < 0 — ValueError.
    2. Если items_total >= 3000 — доставка бесплатна.
    3. Иначе стоимость доставки:
       - distance_km <= 3: 150
       - 3 < distance_km <= 10: 300
       - distance_km > 10: 300 + (distance_km - 10) * 25
    4. Для premium-пользователя скидка 20% на стоимость доставки.
    5. Итоговая сумма = items_total + стоимость доставки.
    """
    if items_total < 0:
        raise ValueError("items_total must be >= 0")
    if distance_km < 0:
        raise ValueError("distance_km must be >= 0")

    if items_total >= 3000:
        delivery_cost = 0.0
    elif distance_km <= 3:
        delivery_cost = 150.0
    elif distance_km <= 10:
        delivery_cost = 300.0
    else:
        delivery_cost = 300.0 + (distance_km - 10) * 25.0

    if is_premium:
        delivery_cost *= 0.8

    return items_total + delivery_cost