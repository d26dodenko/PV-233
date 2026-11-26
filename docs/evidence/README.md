# Доказательства фактических проверок

Дата: 26.11.2026. Среда: Linux x86_64, Python 3.13.11, Rust 1.100.0,
Node.js 24.21.0, Playwright 1.56.1 / Chromium 141.
Все перечисленные результаты получены запуском инструментов, а не заполнены
по ожидаемым значениям. Разные протоколы относятся к своим конкретным прогонам.

| Файл | Что подтверждает |
|---|---|
| [python-tests.txt](python-tests.txt) | 67 pytest PASS, 100% line/branch coverage |
| [rust-tests.txt](../../TestingPS/Laba-3/evidence/rust-tests.txt) | 8 unit + 12 integration PASS |
| [rust-coverage.txt](../../TestingPS/Laba-3/evidence/rust-coverage.txt) | 88,61% line coverage; main.rs не исключён |
| [ui-tests.txt](../../TestingPS/Laba-3/evidence/ui-tests.txt), [JUnit](../../TestingPS/Laba-3/evidence/ui-junit.xml) | 6 E2E PASS на release binary |
| [ui-success.png](../../TestingPS/Laba-3/evidence/ui-success.png) | Настоящая страница успешно оформленного заказа |
| [ui-failed-locator.txt](../../TestingPS/Laba-3/evidence/ui-failed-locator.txt), [скриншот](../../TestingPS/Laba-3/evidence/ui-failed-locator.png) | Первоначальный дефект селектора автотеста, затем исправленный |
| [package-smoke.json](../../TestingPS/Laba-3/evidence/package-smoke.json) | Пять HTTP 200 после распаковки release в отдельный каталог |
| [metrics.json](../../Specification/Laba-1/evidence/metrics.json) | Измеренные Radon LOC/SLOC/CC и coverage обоих Python-модулей |
| [api-results.md](../../TestingPS/Laba-2/evidence/api-results.md), [JSON](../../TestingPS/Laba-2/evidence/api-results.json) | Реальный Newman: 36 запросов, 118 assertions, 7 failures |
| [gate-unit.txt](../../TestingPS/Laba-3/evidence/gate-unit.txt) | Настоящий pytest отказ, exit 1 |
| [gate-coverage.txt](../../TestingPS/Laba-3/evidence/gate-coverage.txt) | 66,67% < 80%, exit 1 |
| [gate-security.txt](../../TestingPS/Laba-3/evidence/gate-security.txt) | Bandit B602 High, exit 1 |
| [gate-critical.txt](../../TestingPS/Laba-3/evidence/gate-critical.txt) | Отказ gate при Critical в реальном исходном audit |
| [security-before.json](../../TestingPS/Laba-3/evidence/security-before.json) | Снимок исходной Critical зависимости и npm metadata |
| [security.json](../../TestingPS/Laba-3/evidence/security.json) | После исправления: Critical 0; Rust/Python аудит без находок; dev High отражены |

Дополнительные локальные проверки: Ruff, rustfmt, Clippy с запретом warnings,
TypeScript typecheck, ESLint и Vite build, `actionlint`, разбор GitLab YAML,
сверка CI-графа и коллекции, проверка относительных ссылок и идентичности
копий исходных заданий. Сбой инструментов или found defects не маскировались.

Большие HTML/XML/LCOV/trace/video и выпускной архив лежат в игнорируемом
`artifacts/`; CI загрузит их в artifacts своего прогона. Полный Newman JSON
не добавлен в Git: может содержать выданный token.

**Отсутствующие внешние доказательства:** hosted GitHub/GitLab pipeline,
административная branch protection и GUI Postman Runner. Их наличие здесь
не утверждается; инструкции приведены в отчётах API и CI/CD.
