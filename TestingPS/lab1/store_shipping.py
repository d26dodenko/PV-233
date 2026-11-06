"""Расчёт стоимости доставки интернет-магазина."""


def calculate_shipping(order_sum: float, item_count: int,
                       express: bool, premium: bool) -> float:
    """Вернуть стоимость доставки с учётом заказа и статуса клиента."""
    if order_sum < 0:
        raise ValueError("Сумма заказа не может быть отрицательной")
    if item_count < 1:
        raise ValueError("Количество товаров должно быть больше нуля")

    # Бесплатная обычная доставка при сумме от 3000 рублей.
    if order_sum >= 3000 and not express:
        return 0.0

    # Базовый тариф зависит от количества товаров.
    if item_count <= 3:
        cost = 180.0
    elif item_count <= 10:
        cost = 350.0
    else:
        cost = 350.0 + (item_count - 10) * 25.0

    if express:
        cost += 120.0
    if premium:
        cost *= 0.8

    return round(cost, 2)
