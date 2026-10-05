# Лабораторная работа №1 <br> Составление тест-кейсов для готового кода. Качество ПО и место тестирования в жизненном цикле

## Выполненная работа — Мороз Роман

Ветка: `moroz_roman`. Функция из задания реализована в [delivery.py](delivery.py),
34 автотеста — в [tests/test_delivery.py](tests/test_delivery.py).
Анализ правил, классы эквивалентности, тест-кейсы и выводы:
[отчёт](docs/report.md). Исходное задание сохранено ниже.

### Запуск через uv

Требуется [uv](https://docs.astral.sh/uv/getting-started/installation/).
Локальная версия Python задана в `.python-version` (3.13).

```bash
uv sync --locked --dev
uv run --locked pytest -v
```

`uv sync` создаёт `.venv` и устанавливает зависимости из `uv.lock`.
При необходимости uv автоматически скачивает Python. Активировать `.venv`
для `uv run` не требуется. Эквивалентный запуск команды из задания:

```bash
source .venv/bin/activate
pytest -v
```

Проверка покрытия строк и ветвей, как в CI:

```bash
uv run --locked pytest -v --cov=delivery --cov-branch --cov-report=term-missing --cov-report=xml --junitxml=test-results.xml
```

[GitHub Actions](.github/workflows/tests.yml) запускает эту проверку на Python
3.11, 3.12, 3.13 и 3.14 при push, pull request и вручную. Для успешной
проверки необходимо 100% покрытия строк и ветвей `delivery.py`.
Зависимости устанавливаются с `--locked`: рассогласование `pyproject.toml`
и `uv.lock` завершает CI ошибкой. Настройка uv основана на
[официальном руководстве](https://docs.astral.sh/uv/guides/integration/github/).

---
## Цель работы

Сформировать системное представление о качестве ПО и роли тестирования в жизненном цикле; приобрести практические навыки проектирования тест-кейсов и написания автотестов на основе готового кода.

**Задачи:**

1. Проанализировать готовый модуль и выделить бизнес-правила, входные и выходные данные, ограничения.
2. Составить набор тест-кейсов: позитивных, негативных, граничных, покрывающих эквивалентные классы.
3. Оформить тест-кейсы по стандартным атрибутам.
4. Реализовать автотесты на Python + pytest.
5. Запустить тесты и зафиксировать результаты.
6. Сделать вывод о связи тестирования, качества ПО и жизненного цикла.

## Задание:

1. Изучить исходный код и выписать все бизнес-правила.
2. Определить:
   - входные параметры;
   - выходной параметр;
   - допустимые и недопустимые значения;
   - граничные значения.
3. Составить **не менее 10 тест-кейсов**:
   - позитивные;
   - негативные;
   - граничные;
   - проверяющие скидку для premium-пользователей;
   - проверяющие бесплатную доставку.
4. Написать автотесты на `pytest`.
5. Запустить тесты командой `pytest -v`.
6. Сделать вывод: какие ветви кода покрыты, какие риски остались, почему тестирование важно для качества.

## 3. ПРИМЕР - Исходный код

```python
# delivery.py

def calculate_delivery_cost(order_amount: float, distance_km: float, is_premium: bool) -> float:
    """
    Расчёт стоимости доставки.

    Бизнес-правила:
    1. Если order_amount < 0 или distance_km < 0 — ValueError.
    2. Если order_amount >= 5000 — доставка бесплатна (0).
    3. Иначе:
       - distance_km <= 5: 200
       - 5 < distance_km <= 20: 500
       - distance_km > 20: 500 + (distance_km - 20) * 30
    4. Для is_premium=True применяется скидка 50% на стоимость доставки.
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
```

## 4. Реализация автотестов

```python
# test_delivery.py

import pytest
from delivery import calculate_delivery_cost


# test_delivery.py

import pytest
from delivery import calculate_delivery_cost


def test_free_delivery_from_5000():
    # Сумма 5000 — доставка бесплатная
    assert calculate_delivery_cost(5000, 10, False) == 0.0


def test_paid_delivery_below_5000():
    # Сумма 4999.99 — доставка платная
    assert calculate_delivery_cost(4999.99, 10, False) == 500.0


def test_short_distance():
    # До 5 км — тариф 200
    assert calculate_delivery_cost(1000, 5, False) == 200.0


def test_middle_distance():
    # От 5 до 20 км — тариф 500
    assert calculate_delivery_cost(1000, 20, False) == 500.0


def test_long_distance():
    # Больше 20 км — 500 + 30 за каждый км
    assert calculate_delivery_cost(1000, 30, False) == 800.0


def test_premium_discount():
    # Premium — скидка 50%
    assert calculate_delivery_cost(1000, 10, True) == 250.0


def test_negative_order_amount():
    # Отрицательная сумма — ошибка
    with pytest.raises(ValueError):
        calculate_delivery_cost(-1, 10, False)


def test_negative_distance():
    # Отрицательное расстояние — ошибка
    with pytest.raises(ValueError):
        calculate_delivery_cost(1000, -1, False)
```
