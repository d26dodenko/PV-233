"""Генератор коллекции и трассируемого каталога API-кейсов."""

import json
from pathlib import Path

POSTMAN_DIR = Path(__file__).resolve().parents[1] / "postman"

folders = {name: [] for name in ("Auth", "Booking", "Health")}
cases = []


def request(
    case_id,
    folder,
    title,
    method,
    path,
    status,
    body=None,
    checks=None,
    token=None,
    pre=None,
    save=None,
    category="positive",
):
    description = (
        f"{case_id}. {title}. Тип: {category}. "
        f"Вход: {method} {path}; тело приведено в Body. "
        f"Ожидается HTTP {status}; задержка < 2000 мс. "
        "Выполнять коллекцию целиком по порядку. Изменяются только созданные этим прогоном записи."
    )
    script = [
        f'pm.test("{case_id}: HTTP {status}", () => pm.response.to.have.status({status}));',
        'pm.test("Ответ быстрее 2000 мс", () => pm.expect(pm.response.responseTime).to.be.below(2000));',
        'pm.test("Ответ не пустой", () => pm.expect(pm.response.text().length).to.be.above(0));',
    ]
    script += checks or []
    if save:
        script += [
            f'if (pm.response.code === 200) {{ const data = pm.response.json(); if (data.{save[1]}) pm.environment.set("{save[0]}", data.{save[1]}); }}'
        ]
    headers = [{"key": "Accept", "value": "application/json"}]
    if body is not None:
        headers.append({"key": "Content-Type", "value": "application/json"})
    if token:
        headers.append({"key": "Cookie", "value": f"token={token}"})
    item = {
        "name": f"{case_id} {title}",
        "request": {
            "method": method,
            "header": headers,
            "url": "{{baseUrl}}" + path,
            "description": description,
        },
        "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": script}}],
    }
    if body is not None:
        item["request"]["body"] = {
            "mode": "raw",
            "raw": body if isinstance(body, str) else json.dumps(body, ensure_ascii=False),
            "options": {"raw": {"language": "json"}},
        }
    if pre:
        item["event"].insert(
            0, {"listen": "prerequest", "script": {"type": "text/javascript", "exec": pre}}
        )
    folders[folder].append(item)
    cases.append(
        {
            "id": case_id,
            "name": title,
            "method": method,
            "path": path,
            "category": category,
            "expected_status": status,
            "body": body,
        }
    )


booking = {
    "firstname": "{{runName}}",
    "lastname": "Moroz",
    "totalprice": 120,
    "depositpaid": True,
    "bookingdates": {"checkin": "2027-01-10", "checkout": "2027-01-12"},
    "additionalneeds": "Breakfast",
}
request(
    "API-01",
    "Auth",
    "Получить токен",
    "POST",
    "/auth",
    200,
    {"username": "admin", "password": "password123"},
    checks=[
        'pm.test("Токен непустой", () => pm.expect(pm.response.json().token).to.be.a("string").and.not.empty);'
    ],
    save=("token", "token"),
    pre=[
        'pm.environment.unset("token"); pm.environment.unset("bookingId"); pm.environment.unset("probeId");',
        'pm.environment.set("runName", "Moroz_" + Date.now() + "_" + Math.random().toString(16).slice(2,8));',
    ],
)
request(
    "API-02",
    "Auth",
    "Неверный пароль: документированная особенность HTTP 200",
    "POST",
    "/auth",
    200,
    {"username": "admin", "password": "wrong"},
    category="negative",
    checks=[
        'pm.test("Ошибка авторизации без токена", () => { const data = pm.response.json(); pm.expect(data.reason).to.eql("Bad credentials"); pm.expect(data).not.to.have.property("token"); });'
    ],
)
request(
    "API-03",
    "Auth",
    "Неверный логин",
    "POST",
    "/auth",
    200,
    {"username": "wrong", "password": "password123"},
    category="negative",
    checks=[
        'pm.test("Нет токена", () => pm.expect(pm.response.json()).not.to.have.property("token"));'
    ],
)
request(
    "API-04",
    "Booking",
    "Создать бронирование",
    "POST",
    "/booking",
    200,
    booking,
    save=("bookingId", "bookingid"),
    checks=[
        'pm.test("Схема ответа", () => { const d = pm.response.json(); pm.expect(d.bookingid).to.be.a("number"); pm.expect(d.booking.totalprice).to.eql(120); pm.expect(d.booking.firstname).to.eql(pm.environment.get("runName")); });'
    ],
)
request(
    "API-05",
    "Booking",
    "Список и фильтр по имени",
    "GET",
    "/booking?firstname={{runName}}",
    200,
    checks=[
        'pm.test("Список содержит наше бронирование", () => pm.expect(pm.response.json().map(b => b.bookingid)).to.include(Number(pm.environment.get("bookingId"))));'
    ],
)
request(
    "API-06",
    "Booking",
    "Получить созданную запись",
    "GET",
    "/booking/{{bookingId}}",
    200,
    checks=[
        'pm.test("Все поля сохранены", () => { const d = pm.response.json(); pm.expect(d.firstname).to.eql(pm.environment.get("runName")); pm.expect(d.totalprice).to.eql(120); pm.expect(d.depositpaid).to.eql(true); pm.expect(d.bookingdates).to.deep.eql({checkin:"2027-01-10",checkout:"2027-01-12"}); });'
    ],
)
updated = {**booking, "totalprice": 250, "additionalneeds": "Dinner"}
request(
    "API-07",
    "Booking",
    "Полное обновление PUT",
    "PUT",
    "/booking/{{bookingId}}",
    200,
    updated,
    token="{{token}}",
    checks=[
        'pm.test("Обновлены цена и услуга", () => { pm.expect(pm.response.json().totalprice).to.eql(250); pm.expect(pm.response.json().additionalneeds).to.eql("Dinner"); });'
    ],
)
request(
    "API-08",
    "Booking",
    "Частичное обновление PATCH",
    "PATCH",
    "/booking/{{bookingId}}",
    200,
    {"lastname": "Updated"},
    token="{{token}}",
    checks=[
        'pm.test("Изменено только указанное поле", () => { pm.expect(pm.response.json().lastname).to.eql("Updated"); pm.expect(pm.response.json().totalprice).to.eql(250); });'
    ],
)
request(
    "API-09",
    "Booking",
    "Обновление сохранено при GET",
    "GET",
    "/booking/{{bookingId}}",
    200,
    checks=[
        'pm.test("PUT и PATCH персистентны", () => { pm.expect(pm.response.json().lastname).to.eql("Updated"); pm.expect(pm.response.json().totalprice).to.eql(250); });'
    ],
)
request(
    "API-10",
    "Booking",
    "PUT без токена",
    "PUT",
    "/booking/{{bookingId}}",
    403,
    updated,
    category="negative",
)
request(
    "API-11",
    "Booking",
    "PATCH с неверным токеном",
    "PATCH",
    "/booking/{{bookingId}}",
    403,
    {"lastname": "Intruder"},
    token="invalid",
    category="negative",
)
request(
    "API-12",
    "Booking",
    "DELETE без токена",
    "DELETE",
    "/booking/{{bookingId}}",
    403,
    category="negative",
)
request(
    "API-13",
    "Booking",
    "Негативные проверки не изменили запись",
    "GET",
    "/booking/{{bookingId}}",
    200,
    checks=[
        'pm.test("Запись не изменена", () => pm.expect(pm.response.json().lastname).to.eql("Updated"));'
    ],
)
request(
    "API-14", "Booking", "Несуществующий ID", "GET", "/booking/2147483647", 404, category="negative"
)
request(
    "API-15",
    "Booking",
    "Синтаксически неверный JSON",
    "POST",
    "/booking",
    400,
    '{"firstname":',
    category="negative",
)
probes = [
    (
        "API-16",
        "Строка вместо totalprice",
        {**booking, "totalprice": "not-a-number"},
        400,
        "negative",
    ),
    ("API-17", "Отсутствуют обязательные поля", {"firstname": "{{runName}}"}, 400, "negative"),
    ("API-18", "Пустые имена", {**booking, "firstname": "", "lastname": ""}, 400, "boundary"),
    ("API-19", "Имя длиной 1001 символ", {**booking, "firstname": "M" * 1001}, 200, "boundary"),
    ("API-20", "Нулевая цена", {**booking, "totalprice": 0}, 200, "boundary"),
    ("API-21", "Отрицательная цена", {**booking, "totalprice": -1}, 400, "boundary"),
    ("API-22", "Большая цена 2147483647", {**booking, "totalprice": 2147483647}, 200, "boundary"),
    (
        "API-23",
        "Выезд раньше заезда",
        {**booking, "bookingdates": {"checkin": "2027-01-12", "checkout": "2027-01-10"}},
        400,
        "boundary",
    ),
    (
        "API-24",
        "Невалидные даты",
        {**booking, "bookingdates": {"checkin": "not-a-date", "checkout": "not-a-date"}},
        400,
        "boundary",
    ),
]
for cid, title, body, status, kind in probes:
    request(
        cid,
        "Booking",
        title,
        "POST",
        "/booking",
        status,
        body,
        category=kind,
        save=("probeId", "bookingid"),
        pre=['pm.environment.unset("probeId");'],
    )
    request(
        cid + "-C",
        "Booking",
        "Удалить только запись текущего probe",
        "DELETE",
        "/booking/{{probeId}}",
        201,
        token="{{token}}",
        category="cleanup",
        pre=['if (!pm.environment.get("probeId")) pm.execution.skipRequest();'],
    )
request(
    "API-25",
    "Booking",
    "Удаление: документированный HTTP 201",
    "DELETE",
    "/booking/{{bookingId}}",
    201,
    token="{{token}}",
)
request(
    "API-26",
    "Booking",
    "GET удалённой записи",
    "GET",
    "/booking/{{bookingId}}",
    404,
    category="negative",
)
request(
    "API-27",
    "Booking",
    "Повторное удаление: особенность HTTP 405",
    "DELETE",
    "/booking/{{bookingId}}",
    405,
    token="{{token}}",
    category="negative",
)
request("API-28", "Health", "Проверка доступности: документированный HTTP 201", "GET", "/ping", 201)
collection = {
    "info": {
        "name": "LabAPI_Moroz",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        "description": "Мороз Роман. Строгие ожидания для негативных входов: обнаруженные дефекты дают красные проверки. HTTP 200 auth/POST и 201 DELETE/ping сохранены по контракту Restful-Booker. Порядок: Auth → Booking → Health. Только свои bookingId/probeId.",
    },
    "item": [{"name": name, "item": items} for name, items in folders.items()],
}
POSTMAN_DIR.mkdir(exist_ok=True)
(POSTMAN_DIR / "LabAPI_Moroz.postman_collection.json").write_text(
    json.dumps(collection, ensure_ascii=False, indent=2) + "\n"
)
env = {
    "name": "Restful Booker — Moroz",
    "values": [
        {"key": k, "value": v, "enabled": True, "type": "default"}
        for k, v in [
            ("baseUrl", "https://restful-booker.herokuapp.com"),
            ("token", ""),
            ("bookingId", ""),
            ("probeId", ""),
            ("runName", ""),
        ]
    ],
    "_postman_variable_scope": "environment",
}
(POSTMAN_DIR / "local.postman_environment.json").write_text(
    json.dumps(env, ensure_ascii=False, indent=2) + "\n"
)
(POSTMAN_DIR / "cases.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2) + "\n")
print(f"Generated {len(cases)} requests, all with >= 3 checks")
