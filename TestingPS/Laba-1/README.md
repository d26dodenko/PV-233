# Лабораторная работа №1 — тестирование расчёта доставки

**Предмет:** тестирование программных систем. **Автор:** Мороз Роман, ПВ-233.
Исходное задание: `TestingPS/Laba-1.md` из `main`.

| Материал | Содержание |
|---|---|
| [assignment.md](assignment.md) | Полный оригинальный текст задания |
| [report.md](report.md) | Бизнес-правила, классы эквивалентности, 34 тест-кейса, риски и выводы |
| [delivery.py](delivery.py) | Расчёт стоимости доставки |
| [tests/test_delivery.py](tests/test_delivery.py) | Позитивные, негативные и граничные автотесты |
| [evidence/test-results.txt](evidence/test-results.txt) | Актуальный отдельный прогон работы |
| [evidence/initial-test-results.txt](evidence/initial-test-results.txt) | Первоначальный исторический протокол |

Команды **из корня репозитория**:

```bash
uv sync --locked --dev
uv run --locked pytest -v TestingPS/Laba-1/tests
```

Результат: **34 passed**. Общее измерение покрытия доставки и калькулятора
описано в [главном README](../../README.md).
