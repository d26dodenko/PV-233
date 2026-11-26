# Лабораторная работа №3 — UI-автоматизация и CI/CD

**Предмет:** тестирование программных систем. **Автор:** Мороз Роман, ПВ-233.
Номер каталога соответствует `TestingPS/Laba-3.md` из `main`; в оригинальном
заголовке задания указано №4.

| Материал | Содержание |
|---|---|
| [assignment.md](assignment.md) | Полный оригинальный текст задания |
| [report.md](report.md) | UI-сценарии, Page Object, пирамида, прогоны и выводы |
| [ci-cd.md](ci-cd.md) | Разбор обоих pipeline, quality gates, branch protection и контрольные вопросы |
| [src/](src/) и [Cargo.toml](Cargo.toml) | Rust/Axum backend магазина |
| [tests/shop_api.rs](tests/shop_api.rs) | HTTP integration tests |
| [frontend/](frontend/) | Адаптированный React UI |
| [e2e/](e2e/) и [playwright.config.ts](playwright.config.ts) | Браузерные тесты с Page Objects |
| [scripts/](scripts/) | Демонстрации отказов gates и проверка выпускного пакета |
| [evidence/](evidence/) | Реальные логи, скриншоты, security и coverage |
| [THIRD_PARTY.md](THIRD_PARTY.md) | Происхождение адаптированного интерфейса |
| [GitHub Actions](../../.github/workflows/ci.yml), [GitLab CI](../../.gitlab-ci.yml) | Рабочие конфиги в обязательных для платформ местах |

Команды **из корня репозитория**:

```bash
npm ci
npm --prefix TestingPS/Laba-3/frontend ci
npm --prefix TestingPS/Laba-3/frontend run build
cargo test --locked
npx playwright install --with-deps chromium
npm run test:e2e
```

Запуск приложения: `cargo run --locked`, открыть <http://127.0.0.1:3000>.
Cargo workspace в корне включает Rust-проект этой лабораторной.
Результат: **8 unit + 12 integration + 6 E2E**. Инструкции по hosted CI и
административной настройке `main` приведены в `ci-cd.md`.
