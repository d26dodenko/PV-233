import pytest
from store_shipping import calculate_shipping


@pytest.mark.parametrize(
    "order_sum, item_count, express, premium, expected",
    [
        (1000, 1, False, False, 180.0),     # TC01: минимум товаров
        (1000, 3, False, False, 180.0),     # TC02: граница 3 товара
        (1000, 4, False, False, 350.0),     # TC03: граница 4 товара
        (1000, 10, False, False, 350.0),    # TC04: граница 10 товаров
        (1000, 11, False, False, 375.0),    # TC05: граница 11 товаров
        (1000, 15, False, False, 475.0),    # TC06: более 10 товаров
        (1000, 1, True, False, 300.0),      # TC07: экспресс
        (1000, 4, True, False, 470.0),      # TC08: экспресс для 4 товаров
        (1000, 1, False, True, 144.0),      # TC09: premium-скидка
        (1000, 10, False, True, 280.0),     # TC10: premium для 10 товаров
        (1000, 11, True, True, 396.0),      # TC11: экспресс и premium
        (2999.99, 3, False, False, 180.0), # TC12: ниже порога бесплатной доставки
        (3000, 3, False, False, 0.0),       # TC13: порог бесплатной доставки
        (4000, 15, False, False, 0.0),      # TC14: выше порога
        (3000, 1, True, False, 300.0),     # TC15: экспресс не бывает бесплатным
        (0, 1, False, False, 180.0),        # TC16: нулевая сумма заказа
        (3000, 1, False, True, 0.0),       # TC17: premium и бесплатная доставка
    ],
    ids=[f"TC{i:02d}" for i in range(1, 18)],
)
def test_calculate_shipping(order_sum, item_count, express, premium, expected):
    assert calculate_shipping(order_sum, item_count, express, premium) == expected


@pytest.mark.parametrize(
    "order_sum, item_count, express, premium",
    [
        (-1, 1, False, False),       # TC18: отрицательная сумма
        (1000, 0, False, False),     # TC19: ноль товаров
        (1000, -1, False, False),    # TC20: отрицательное количество
        (3000, 0, False, False),     # TC21: ошибка важнее бесплатной доставки
    ],
    ids=[f"TC{i:02d}" for i in range(18, 22)],
)
def test_invalid_inputs(order_sum, item_count, express, premium):
    with pytest.raises(ValueError):
        calculate_shipping(order_sum, item_count, express, premium)
