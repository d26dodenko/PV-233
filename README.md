# Лабораторные работы · Мороз Роман · ПВ-233

[![CI](https://github.com/d26dodenko/PV-233/actions/workflows/ci.yml/badge.svg?branch=moroz_roman)](https://github.com/d26dodenko/PV-233/actions/workflows/ci.yml)

Ветка `moroz_roman`. Работы разделены по предметам, как в `main`:
**[TestingPS — тестирование программных систем](TestingPS/README.md)** и
**[Specification — спецификация и качество ПО](Specification/README.md)**.
В каждой работе есть полное задание в `assignment.md`, навигация в `README.md`,
отчёт и относящиеся к ней исходники, тесты и результаты.

## Структура

```text
TestingPS/
├── README.md
├── Laba-1/                 # Тест-кейсы и pytest: доставка
│   ├── assignment.md
│   ├── README.md
│   ├── report.md
│   ├── delivery.py
│   ├── tests/
│   └── evidence/
├── Laba-2/                 # API: Postman и Newman
│   ├── assignment.md
│   ├── README.md
│   ├── report.md
│   ├── postman/
│   ├── scripts/
│   └── evidence/
└── Laba-3/                 # UI, пирамида и CI/CD
    ├── assignment.md
    ├── README.md
    ├── report.md
    ├── ci-cd.md
    ├── Cargo.toml
    ├── src/
    ├── tests/
    ├── frontend/
    ├── e2e/
    ├── scripts/
    └── evidence/
Specification/
├── README.md
├── Laba-1/                 # Калькулятор и метрики качества
│   ├── assignment.md
│   ├── README.md
│   ├── report.md
│   ├── calculator.py
│   ├── tests/
│   ├── scripts/
│   ├── tasks.md
│   └── evidence/
└── Total/                  # Итоговое проектирование
    ├── assignment.md
    ├── README.md
    ├── report.md
    ├── technical-specification.md
    └── kanban.md
```

В корне находятся общие зависимости и конфиги запуска: `pyproject.toml`,
`uv.lock`, `package.json`, `package-lock.json`, Cargo workspace, Rust toolchain,
`.github/workflows/` и `.gitlab-ci.yml`. `docs/` содержит только общую матрицу
приёмки и сводку проверок. Выполнение каждой работы находится внутри её предмета.

## Навигация по заданиям

| Предмет | Работа | Задание | Выполнение |
|---|---|---|---|
| Тестирование | №1: расчёт доставки | [Условие](TestingPS/Laba-1/assignment.md) | [Лабораторная](TestingPS/Laba-1/README.md) |
| Тестирование | №2: API | [Условие](TestingPS/Laba-2/assignment.md) | [Лабораторная](TestingPS/Laba-2/README.md) |
| Тестирование | №3: UI и CI/CD | [Условие](TestingPS/Laba-3/assignment.md) | [Лабораторная](TestingPS/Laba-3/README.md) |
| Спецификация | №1: качество и метрики | [Условие](Specification/Laba-1/assignment.md) | [Лабораторная](Specification/Laba-1/README.md) |
| Спецификация | Итоговое проектирование | [Условие](Specification/Total/assignment.md) | [Итоговая работа](Specification/Total/README.md) |

Нумерация каталогов соответствует исходным файлам в `main`. Внутри задания
API указан №3, внутри задания UI — №4; оригинальные заголовки сохранены.

## Установка и общий запуск

Требуются Linux, Python 3.13 через uv, Node.js 24/npm, Rust через rustup.
Все команды ниже выполняются **из корня репозитория**:

```bash
uv sync --locked --dev
cargo fetch --locked
npm ci
npm --prefix TestingPS/Laba-3/frontend ci
npm --prefix TestingPS/Laba-3/frontend run build
npx playwright install --with-deps chromium
```

Точные зависимости зафиксированы lockfiles. Команды отдельных лабораторных
приведены в их `README.md`. Общий набор проверок:

```bash
# 34 теста доставки и 33 теста калькулятора.
uv run --locked pytest -v
uv run --locked pytest --cov --cov-branch \
  --cov-report=term-missing --cov-report=xml:artifacts/python/coverage.xml \
  --junitxml=artifacts/python/junit.xml

# Rust unit и HTTP integration третьей работы.
cargo test --locked
cargo fmt --all --check
cargo clippy --locked --all-targets -- -D warnings

# Браузерные E2E третьей работы.
npm run typecheck
npm --prefix TestingPS/Laba-3/frontend run lint
npm run test:e2e
```

Запуск магазина: `cargo run --locked`, открыть <http://127.0.0.1:3000>.
Хранилище учебное, в памяти процесса. Playwright сам запускает сервер для тестов.
Rust coverage: `cargo llvm-cov --locked --all-targets --fail-under-lines 80`;
инструмент установки и подробные отчёты описаны в третьей лабораторной.
Python lint: `uv run --locked ruff check .` и `uv run --locked ruff format --check .`.

## CI/CD и результаты

[GitHub Actions](.github/workflows/ci.yml) и [GitLab CI](.gitlab-ci.yml):
unit/lint/security → build → integration/coverage → E2E → release candidate.
[Пояснения обоих конфигов](TestingPS/Laba-3/ci-cd.md) находятся в третьей работе.
[API workflow](.github/workflows/api.yml) проверяет публичный сервис отдельно:
найденные расхождения дают честный failed статус.

Подготовленный набор: **67 Python + 8 Rust unit + 12 Rust integration + 6 E2E = 93 теста**.
Python coverage — 100% строк и ветвей; Rust gate — 80% строк.
[Матрица выполнения](docs/acceptance.md) и [сводка доказательств](docs/evidence/README.md)
связывают требования с конкретными материалами работ.

Изменения локальные. Hosted CI, административная защита main и GUI-скриншот
Postman Runner остаются внешними шагами; инструкции и ограничения сохранены
в соответствующих отчётах.
