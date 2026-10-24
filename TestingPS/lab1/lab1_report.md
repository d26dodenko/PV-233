# Лабораторная работа №1

**Тема:** Составление тест-кейсов для готового кода. Качество ПО и место тестирования в жизненном цикле

---

## 1. Цель работы

Сформировать представление о качестве ПО и роли тестирования в жизненном цикле, получить практические навыки проектирования тест-кейсов и написания автотестов на Python + pytest.

## 2. Анализ исходного кода

Тестируемая функция: `calculate_delivery_cost(order_amount, distance_km, is_premium)` (файл `delivery.py`).

### 2.1. Бизнес-правила

1. Если `order_amount < 0` или `distance_km < 0` — выбрасывается `ValueError`.
2. Если `order_amount >= 3000` — доставка бесплатна (0).
3. Иначе стоимость зависит от расстояния:
   - `distance_km <= 3` — 150;
   - `3 < distance_km <= 15` — 400;
   - `distance_km > 15` — `400 + (distance_km - 15) * 25`.
4. Для `is_premium=True` на стоимость доставки действует скидка 30%.

### 2.2. Входные и выходные данные

| Параметр | Тип | Допустимые значения | Недопустимые значения |
|---|---|---|---|
| `order_amount` | float | `>= 0` | `< 0` |
| `distance_km` | float | `>= 0` | `< 0` |
| `is_premium` | bool | `True`, `False` | — |
| **Результат** | float | стоимость доставки `>= 0` | `ValueError` при неверных данных |

### 2.3. Граничные значения

- `order_amount`: `0`, `2999.99`, `3000`.
- `distance_km`: `0`, `3`, `3.01`, `15`, `16`.

## 3. Тест-кейсы

| ID | Тип | Входные данные (сумма, км, premium) | Ожидаемый результат |
|---|---|---|---|
| TC-01 | Позитивный | 1000, 2, False | 150 |
| TC-02 | Позитивный | 1000, 10, False | 400 |
| TC-03 | Позитивный | 1000, 25, False | 650 |
| TC-04 | Негативный | -1, 10, False | `ValueError` (order_amount) |
| TC-05 | Негативный | 100, -10, False | `ValueError` (distance_km) |
| TC-06 | Негативный | -1, -10, False | `ValueError` (order_amount) |
| TC-07 | Граничный | 1000, 0, False | 150 |
| TC-08 | Граничный | 1000, 3, False | 150 |
| TC-09 | Граничный | 1000, 3.01, False | 400 |
| TC-10 | Граничный | 1000, 15, False | 400 |
| TC-11 | Граничный | 1000, 16, False | 425 |
| TC-12 | Premium | 1000, 10, True | 280 |
| TC-13 | Premium | 2000, 2, True | 105 |
| TC-14 | Бесплатная доставка | 3000, 10, False | 0 |
| TC-15 | Граничный (сумма) | 2999.99, 10, False | 400 |
| TC-16 | Бесплатная доставка | 10000, 100, False | 0 |
| TC-17 | Граничный (сумма) | 0, 10, False | 400 |

Всего: 17 тест-кейсов (позитивные, негативные, граничные, на скидку premium и на бесплатную доставку).

## 4. Реализация автотестов

Автотесты написаны на Python + pytest и находятся в файле `test_delivery.py`. Для проверки исключений используется `pytest.raises` с параметром `match` (проверка текста ошибки), для сравнения дробных чисел — `pytest.approx` (из-за погрешности float).

## 5. Результаты запуска

Команда: `pytest -v`

```
collected 17 items

lab1/test_delivery.py::test_tc01_short_distance PASSED                    [  5%]
lab1/test_delivery.py::test_tc02_middle_distance PASSED                    [ 11%]
lab1/test_delivery.py::test_tc03_long_distance PASSED                      [ 17%]
lab1/test_delivery.py::test_tc04_negative_order_amount PASSED              [ 23%]
lab1/test_delivery.py::test_tc05_negative_distance_km PASSED               [ 29%]
lab1/test_delivery.py::test_tc06_negative_both PASSED                      [ 35%]
lab1/test_delivery.py::test_tc07_distance_km_zero PASSED                   [ 41%]
lab1/test_delivery.py::test_tc08_distance_exactly_3 PASSED                  [ 47%]
lab1/test_delivery.py::test_tc09_distance_just_above_3 PASSED               [ 52%]
lab1/test_delivery.py::test_tc10_distance_exactly_15 PASSED                 [ 58%]
lab1/test_delivery.py::test_tc11_distance_just_above_15 PASSED              [ 64%]
lab1/test_delivery.py::test_tc12_with_premium PASSED                        [ 70%]
lab1/test_delivery.py::test_tc13_with_premium_short_distance PASSED         [ 76%]
lab1/test_delivery.py::test_tc14_free_delivery_exactly_3000 PASSED          [ 82%]
lab1/test_delivery.py::test_tc15_paid_delivery_just_below_3000 PASSED       [ 88%]
lab1/test_delivery.py::test_tc16_free_delivery_far_distance PASSED          [ 94%]
lab1/test_delivery.py::test_tc17_order_amount_zero PASSED                   [100%]

============================== 17 passed ==============================
```

**Итог:** 17 из 17 тестов пройдены.

## 6. Вывод

**Покрытые ветви.** Тесты покрывают обе проверки на `ValueError`, ветку бесплатной доставки, все три тарифные зоны (до 3 км, 3–15 км, свыше 15 км) и применение скидки premium.

**Оставшиеся риски:**

- не проверяется тип входных данных (`None`, строки, `NaN`, `inf`);
- при обоих отрицательных параметрах всегда сообщается только об `order_amount`;
- не покрыты сочетания premium с расстоянием свыше 15 км и premium при бесплатной доставке;
- 100% покрытия строк и ветвей не гарантирует отсутствия ошибок в логике — оно показывает лишь, что весь код был выполнен.

**Роль тестирования.** Тестирование помогает убедиться, что программа соответствует бизнес-правилам, и фиксирует требования в виде проверяемых сценариев. Автотесты защищают от регрессий при изменении кода и позволяют быстро проверить результат после правок. Чем раньше в жизненном цикле ПО найден дефект, тем дешевле его исправить, поэтому тестирование напрямую влияет на качество продукта.