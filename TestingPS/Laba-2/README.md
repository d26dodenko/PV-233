# Лабораторная работа №2 — API-тестирование

**Предмет:** тестирование программных систем. **Автор:** Мороз Роман, ПВ-233.
Номер каталога соответствует `TestingPS/Laba-2.md` из `main`; в оригинальном
заголовке задания указано №3.

| Материал | Содержание |
|---|---|
| [assignment.md](assignment.md) | Полный оригинальный текст задания |
| [report.md](report.md) | Тест-дизайн, реальные результаты, расхождения и баг-репорты |
| [postman/](postman/) | LabAPI_Moroz, окружение и каталог кейсов |
| [scripts/generate_postman.py](scripts/generate_postman.py) | Воспроизводимая генерация коллекции |
| [scripts/api_report.py](scripts/api_report.py) | Обезличенная сводка Newman |
| [evidence/api-results.md](evidence/api-results.md) | Фактические статусы и время ответа |

Команды **из корня репозитория**:

```bash
npm ci
npm run test:api
uv run --locked python TestingPS/Laba-2/scripts/api_report.py
```

Для Postman импортировать [коллекцию](postman/LabAPI_Moroz.postman_collection.json)
и [окружение](postman/local.postman_environment.json), выбрать окружение и
запустить всю коллекцию. Скрипты передают token/bookingId автоматически.

Публичный учебный сервис имеет найденные расхождения: ненулевой exit code
Newman не подавляется. Результаты и необходимость отдельного GUI-скриншота
Collection Runner описаны в отчёте.
