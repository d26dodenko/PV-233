# Лабораторная работа №1

**Тема:** Составление тест-кейсов для готового кода. Качество ПО и место тестирования в жизненном цикле

---

## 1. Цель работы

Сформировать представление о качестве ПО и роли тестирования в жизненном цикле, получить практические навыки проектирования тест-кейсов и написания автотестов на Python + pytest.

## 2. Анализ исходного кода

Тестируемая функция: `calculate_shipping(order_sum, item_count, express, premium)` (файл `store_shipping.py`). Она рассчитывает стоимость доставки заказа интернет-магазина с учётом количества товаров, срочности доставки и статуса покупателя.

### 2.1. Бизнес-правила

1. Если `order_sum < 0` — выбрасывается `ValueError`.
2. Если `item_count < 1` — выбрасывается `ValueError`.
3. Если `order_sum >= 3000` и `express=False` — доставка бесплатна (0).
4. Иначе базовая стоимость зависит от количества товаров:
   - `1 <= item_count <= 3` — 180 рублей;
   - `4 <= item_count <= 10` — 350 рублей;
   - `item_count > 10` — `350 + (item_count - 10) * 25` рублей.
5. Если `express=True`, к базовой стоимости добавляется 120 рублей. Экспресс-доставка не бывает бесплатной.
6. Для `premium=True` на платную доставку действует скидка 20%.
7. Стоимость доставки округляется до двух знаков после запятой.

### 2.2. Входные и выходные данные

| **Параметр** | **Тип** | **Допустимые значения** | **Недопустимые значения** |
| --- | --- | --- | --- |
| `order_sum` | float | `>= 0` | `< 0` |
| `item_count` | int | целое число `>= 1` | `<= 0` |
| `express` | bool | `True`, `False` | другие типы не проверяются явно |
| `premium` | bool | `True`, `False` | другие типы не проверяются явно |
| **Результат** | float | стоимость доставки `>= 0` | `ValueError` при проверяемых ошибках ввода |

### 2.3. Граничные значения

- `order_sum`: `-1`, `0`, `2999.99`, `3000`, `3000.01`.
- `item_count`: `-1`, `0`, `1`, `3`, `4`, `10`, `11`.
- `express` и `premium`: `False` и `True`.

## 3. Тест-кейсы

| **ID** | **Тип** | **Входные данные (сумма, товары, express, premium)** | **Ожидаемый результат** |
| --- | --- | --- | --- |
| TC-01 | Позитивный | `1000, 1, False, False` | 180 |
| TC-02 | Граничный | `1000, 3, False, False` | 180 |
| TC-03 | Граничный | `1000, 4, False, False` | 350 |
| TC-04 | Граничный | `1000, 10, False, False` | 350 |
| TC-05 | Граничный | `1000, 11, False, False` | 375 |
| TC-06 | Позитивный | `1000, 15, False, False` | 475 |
| TC-07 | Экспресс-доставка | `1000, 1, True, False` | 300 |
| TC-08 | Экспресс-доставка | `1000, 4, True, False` | 470 |
| TC-09 | Premium | `1000, 1, False, True` | 144 |
| TC-10 | Premium | `1000, 10, False, True` | 280 |
| TC-11 | Premium + экспресс | `1000, 11, True, True` | 396 |
| TC-12 | Граничный (сумма) | `2999.99, 3, False, False` | 180 |
| TC-13 | Бесплатная доставка | `3000, 3, False, False` | 0 |
| TC-14 | Бесплатная доставка | `4000, 15, False, False` | 0 |
| TC-15 | Экспресс при большой сумме | `3000, 1, True, False` | 300 |
| TC-16 | Граничный (сумма) | `0, 1, False, False` | 180 |
| TC-17 | Premium + бесплатная доставка | `3000, 1, False, True` | 0 |
| TC-18 | Негативный | `-1, 1, False, False` | `ValueError` (order_sum) |
| TC-19 | Негативный | `1000, 0, False, False` | `ValueError` (item_count) |
| TC-20 | Негативный | `1000, -1, False, False` | `ValueError` (item_count) |
| TC-21 | Негативный | `3000, 0, False, False` | `ValueError` (item_count) |

Всего: **21 тест-кейс** (позитивные, негативные, граничные, на скидку premium, экспресс-доставку и бесплатную доставку).

## 4. Реализация автотестов

Автотесты написаны на Python + pytest и находятся в файле `test_store_shipping.py`. Для передачи наборов входных параметров используется `@pytest.mark.parametrize`, для проверки исключений — `pytest.raises(ValueError)`. Каждому тест-кейсу соответствует отдельный запуск теста с идентификатором от `TC01` до `TC21`.

## 5. Результаты запуска

Команда: `pytest -v`

```text
collected 21 items

test_store_shipping.py::test_calculate_shipping[TC01] PASSED             [  4%]
test_store_shipping.py::test_calculate_shipping[TC02] PASSED             [  9%]
test_store_shipping.py::test_calculate_shipping[TC03] PASSED             [ 14%]
test_store_shipping.py::test_calculate_shipping[TC04] PASSED             [ 19%]
test_store_shipping.py::test_calculate_shipping[TC05] PASSED             [ 23%]
test_store_shipping.py::test_calculate_shipping[TC06] PASSED             [ 28%]
test_store_shipping.py::test_calculate_shipping[TC07] PASSED             [ 33%]
test_store_shipping.py::test_calculate_shipping[TC08] PASSED             [ 38%]
test_store_shipping.py::test_calculate_shipping[TC09] PASSED             [ 42%]
test_store_shipping.py::test_calculate_shipping[TC10] PASSED             [ 47%]
test_store_shipping.py::test_calculate_shipping[TC11] PASSED             [ 52%]
test_store_shipping.py::test_calculate_shipping[TC12] PASSED             [ 57%]
test_store_shipping.py::test_calculate_shipping[TC13] PASSED             [ 61%]
test_store_shipping.py::test_calculate_shipping[TC14] PASSED             [ 66%]
test_store_shipping.py::test_calculate_shipping[TC15] PASSED             [ 71%]
test_store_shipping.py::test_calculate_shipping[TC16] PASSED             [ 76%]
test_store_shipping.py::test_calculate_shipping[TC17] PASSED             [ 80%]
test_store_shipping.py::test_invalid_inputs[TC18] PASSED                 [ 85%]
test_store_shipping.py::test_invalid_inputs[TC19] PASSED                 [ 90%]
test_store_shipping.py::test_invalid_inputs[TC20] PASSED                 [ 95%]
test_store_shipping.py::test_invalid_inputs[TC21] PASSED                 [100%]

============================== 21 passed in 0.05s ==============================
```

**Итог:** 21 из 21 тестов пройдены.

Дополнительно выполнена проверка покрытия командой `pytest --cov=store_shipping --cov-branch --cov-report=term-missing`:

```text
Name                Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------
store_shipping.py      17      0     14      0   100%
---------------------------------------------------------------
TOTAL                  17      0     14      0   100%
```

## 6. Вывод

**Покрытые ветви.** Тесты покрывают проверки отрицательной суммы заказа и недопустимого количества товаров, бесплатную доставку, все три тарифные зоны по количеству товаров, экспресс-доставку и скидку для premium-пользователей.

**Оставшиеся риски:**

- не проверяются типы входных данных (`None`, строки, `NaN`, `inf`);
- не проверяются чрезвычайно большие значения суммы заказа и количества товаров;
- при двух ошибочных параметрах программа сообщает только о первой обнаруженной ошибке;
- 100% покрытия строк и ветвей не гарантирует отсутствия всех ошибок в логике программы.

**Роль тестирования.** Тестирование позволяет проверить соответствие программы бизнес-правилам и выявлять ошибки до использования программы. Автотесты помогают обнаруживать регрессии после изменений в коде. Чем раньше в жизненном цикле ПО обнаружен дефект, тем проще и дешевле его исправить, поэтому тестирование напрямую влияет на качество и надёжность продукта.
