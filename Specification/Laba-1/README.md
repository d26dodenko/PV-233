# Лабораторная работа №1 — качество и метрики ПО

**Предмет:** спецификация и качество ПО. **Автор:** Мороз Роман, ПВ-233.
Исходное задание: `Specification/Laba-1.md` из `main`.

| Материал | Содержание |
|---|---|
| [assignment.md](assignment.md) | Полный оригинальный текст задания |
| [report.md](report.md) | Три проблемы разработки, таблица решений, расчёты и выводы |
| [calculator.py](calculator.py) | Python-калькулятор по требованию задания |
| [tests/test_calculator.py](tests/test_calculator.py) | 33 unit-теста |
| [scripts/metrics.py](scripts/metrics.py) | Измерение LOC, SLOC, CC и покрытия |
| [evidence/metrics.json](evidence/metrics.json) | Фактический снимок метрик |
| [evidence/test-results.txt](evidence/test-results.txt) | Отдельный прогон калькулятора |
| [tasks.md](tasks.md) | Задачи лабораторной в собственной таблице |

Команды **из корня репозитория**:

```bash
uv sync --locked --dev
uv run --locked pytest -v Specification/Laba-1/tests
uv run --locked pytest --cov --cov-branch --cov-report=xml:artifacts/python/coverage.xml
uv run --locked python Specification/Laba-1/scripts/metrics.py
uv run --locked radon cc -s Specification/Laba-1/calculator.py TestingPS/Laba-1/delivery.py
```

Результат: **33 passed**, покрытие строк и ветвей 100%. Общие инструменты и
зависимости устанавливаются из корневых `pyproject.toml` и `uv.lock`.
