# Матрица соответствия исходным заданиям

Автор: Мороз Роман, ПВ-233. Проверка: 26.11.2026.
**Готово** означает наличие артефакта и локальной проверки;
**внешний шаг** означает отсутствие фактического подтверждения hosted/GUI.

| Задание / пункт | Артефакт и подтверждение | Состояние |
|---|---|---|
| Доставка: все бизнес-правила, параметры, классы, границы | [report.md](../TestingPS/Laba-1/report.md), неизменённый алгоритм delivery.py | Готово |
| Доставка: ≥10 позитивных/негативных/граничных кейсов, premium и free | 34 идентифицированных TC, [автотесты](../TestingPS/Laba-1/tests/test_delivery.py) | Готово |
| Доставка: pytest -v, ветви, риски и жизненный цикл | [Свежий протокол](evidence/python-tests.txt), 100% | Готово |
| API: LabAPI_Фамилия, Auth/Booking/Health, переменные | [Collection](../TestingPS/Laba-2/postman/LabAPI_Moroz.postman_collection.json), [environment](../TestingPS/Laba-2/postman/local.postman_environment.json) | Готово |
| API: все восемь endpoints, описания и 3+ проверки | 37 запросов коллекции, [каталог кейсов](../TestingPS/Laba-2/postman/cases.json) | Готово |
| API: автоматические token и bookingId, CRUD без ручных действий | Реальный Newman, основная цепочка и cleanup | Готово |
| API: неверный auth/token/id/JSON/type/обязательные поля | API-02/03/10—17 | Готово |
| API: пустые/1001 символ, 0/−1/большая цена, неверные даты | API-18—24 | Готово |
| API: ожидаемые/фактические коды и таблица расхождений | [36 фактических результатов](../TestingPS/Laba-2/evidence/api-results.md), [6 баг-репортов](../TestingPS/Laba-2/report.md) | Готово, найденные ошибки не скрыты |
| API: запуск и скриншоты GUI Collection Runner | Экспорты и точные шаги запуска в отчёте; выполнен Newman | Внешний шаг: GUI не запускался |
| UI: регистрация, вход, поиск, корзина, заказ, выход | UI-01 через настоящий Chromium | Готово |
| UI: Page Object и дополнительные негативные сценарии | [Page Objects](../TestingPS/Laba-3/e2e/pages.ts), UI-02—06 | Готово |
| UI: успешный и упавший прогоны, скриншоты | [Успех](../TestingPS/Laba-3/evidence/ui-success.png), [падение селектора](../TestingPS/Laba-3/evidence/ui-failed-locator.png), логи | Готово |
| UI: пирамида и обоснование числа тестов | [Пирамида](../TestingPS/Laba-3/report.md): 75 unit / 12 integration / 6 E2E | Готово |
| CI: GitHub Actions + объяснение | [ci.yml](../.github/workflows/ci.yml), [разбор](../TestingPS/Laba-3/ci-cd.md), actionlint без ошибок | Готово локально |
| CI: аналогичный GitLab CI | [.gitlab-ci.yml](../.gitlab-ci.yml), YAML разобран, зависимости проверены | Готово локально; GitLab runner не запускался |
| CI: push/PR, gates, coverage≥80%, vulnerability block | Locked dependencies, needs, exit codes, итоговый required | Готово в конфигурации |
| CI: отчёты и badge | Upload always, JUnit/Cobertura/HTML, badge в README | Готово; badge ждёт удалённого прогона |
| CI: падение unit/coverage/security | [Локальные доказательства](../TestingPS/Laba-3/ci-cd.md), каждый exit 1 | Готово локально |
| CI: скриншот unit failed → Build skipped на GitHub | Граф подготовлен, gate_demo доступен в YAML | Внешний шаг: hosted запуск не выполнен |
| CI: branch protection main | Правильный required check и инструкции в отчёте | Внешний шаг: нужен админ-доступ |
| CI: ответы на четыре контрольных вопроса | [03-ci-cd.md](../TestingPS/Laba-3/ci-cd.md) | Готово |
| Качество: 3 проблемы и таблица решений | [04-quality.md](../Specification/Laba-1/report.md) | Готово |
| Качество: Python-проект, задачи и unit tests | calculator.py, 33 tests, Q-01—Q-05 на [доске](../Specification/Total/kanban.md) | Готово; собственная таблица вместо внешнего трекера |
| Качество: LOC, сложность, дефекты, coverage | [metrics.json](../Specification/Laba-1/evidence/metrics.json), формулы и ограничения в отчёте | Готово |
| Архитектура: описание, 5+ FR и NFR | [05-architecture.md](../Specification/Total/report.md): 10 FR, 7 NFR | Готово |
| Архитектура: монолит, микросервисы, слои со схемами | Три Mermaid-схемы, хранение, взаимодействия, компромиссы | Готово |
| Архитектура: ТЗ | [technical-specification.md](../Specification/Total/technical-specification.md), учебная адаптация требуемой структуры | Готово |
| Архитектура: команда и семь ролей | Четыре проектных участника с совмещением ролей; реальный автор указан | Готово |
| Архитектура: Kanban из шести колонок, ≥20 задач | [34 задачи](../Specification/Total/kanban.md), критерии и зависимости | Готово |

Публикация ветки, hosted прогоны, GUI Postman и административные настройки
не объявлены выполненными. Все доступные локальные реализации, измерения,
конфигурации и отчёты подготовлены; внешние шаги описаны для воспроизведения.
