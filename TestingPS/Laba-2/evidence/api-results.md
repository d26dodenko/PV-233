# Фактические результаты API

Источник: реальный Newman; секреты исключены.

| ID | Запрос | Тип | Ожидалось | Получено | мс | Статус |
|---|---|---|---|---|---|---|
| API-01 | POST /auth | positive | 200 | 200 | 2692 | FAIL |
| API-02 | POST /auth | negative | 200 | 200 | 146 | PASS |
| API-03 | POST /auth | negative | 200 | 200 | 158 | PASS |
| API-04 | POST /booking | positive | 200 | 200 | 165 | PASS |
| API-05 | GET /booking?firstname={{runName}} | positive | 200 | 200 | 157 | PASS |
| API-06 | GET /booking/{{bookingId}} | positive | 200 | 200 | 157 | PASS |
| API-07 | PUT /booking/{{bookingId}} | positive | 200 | 200 | 161 | PASS |
| API-08 | PATCH /booking/{{bookingId}} | positive | 200 | 200 | 159 | PASS |
| API-09 | GET /booking/{{bookingId}} | positive | 200 | 200 | 160 | PASS |
| API-10 | PUT /booking/{{bookingId}} | negative | 403 | 403 | 159 | PASS |
| API-11 | PATCH /booking/{{bookingId}} | negative | 403 | 403 | 159 | PASS |
| API-12 | DELETE /booking/{{bookingId}} | negative | 403 | 403 | 155 | PASS |
| API-13 | GET /booking/{{bookingId}} | positive | 200 | 200 | 463 | PASS |
| API-14 | GET /booking/2147483647 | negative | 404 | 404 | 157 | PASS |
| API-15 | POST /booking | negative | 400 | 400 | 156 | PASS |
| API-16 | POST /booking | negative | 400 | 200 | 156 | FAIL |
| API-16-C | DELETE /booking/{{probeId}} | cleanup | 201 | 201 | 155 | PASS |
| API-17 | POST /booking | negative | 400 | 500 | 156 | FAIL |
| API-18 | POST /booking | boundary | 400 | 200 | 156 | FAIL |
| API-18-C | DELETE /booking/{{probeId}} | cleanup | 201 | 201 | 155 | PASS |
| API-19 | POST /booking | boundary | 200 | 200 | 157 | PASS |
| API-19-C | DELETE /booking/{{probeId}} | cleanup | 201 | 201 | 155 | PASS |
| API-20 | POST /booking | boundary | 200 | 200 | 158 | PASS |
| API-20-C | DELETE /booking/{{probeId}} | cleanup | 201 | 201 | 155 | PASS |
| API-21 | POST /booking | boundary | 400 | 200 | 157 | FAIL |
| API-21-C | DELETE /booking/{{probeId}} | cleanup | 201 | 201 | 156 | PASS |
| API-22 | POST /booking | boundary | 200 | 200 | 155 | PASS |
| API-22-C | DELETE /booking/{{probeId}} | cleanup | 201 | 201 | 159 | PASS |
| API-23 | POST /booking | boundary | 400 | 200 | 155 | FAIL |
| API-23-C | DELETE /booking/{{probeId}} | cleanup | 201 | 201 | 160 | PASS |
| API-24 | POST /booking | boundary | 400 | 200 | 158 | FAIL |
| API-24-C | DELETE /booking/{{probeId}} | cleanup | 201 | 201 | 155 | PASS |
| API-25 | DELETE /booking/{{bookingId}} | positive | 201 | 201 | 155 | PASS |
| API-26 | GET /booking/{{bookingId}} | negative | 404 | 404 | 157 | PASS |
| API-27 | DELETE /booking/{{bookingId}} | negative | 405 | 405 | 161 | PASS |
| API-28 | GET /ping | positive | 201 | 201 | 157 | PASS |
