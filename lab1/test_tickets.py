import pytest
from tickets import calculate_ticket_price


def test_adult_weekday():
    # TC-01: Взрослый билет в будний день — 400 рублей
    assert calculate_ticket_price(25, "weekday", False) == 400.0


def test_adult_weekend():
    # TC-02: Взрослый билет в выходной день — 500 рублей
    assert calculate_ticket_price(25, "weekend", False) == 500.0


def test_age_zero():
    # TC-03: В возрасте 0 лет билет бесплатный
    assert calculate_ticket_price(0, "weekday", False) == 0.0


def test_age_five():
    # TC-04: Ребёнок 5 лет проходит бесплатно, даже со студенческим статусом
    assert calculate_ticket_price(5, "weekend", True) == 0.0


def test_age_six():
    # TC-05: С 6 лет в будни применяется детская скидка 50%
    assert calculate_ticket_price(6, "weekday", False) == 200.0


def test_age_seventeen():
    # TC-06: В 17 лет в выходной билет стоит 250 рублей
    assert calculate_ticket_price(17, "weekend", False) == 250.0


def test_age_eighteen():
    # TC-07: В 18 лет без статуса студента действует обычный тариф
    assert calculate_ticket_price(18, "weekday", False) == 400.0


def test_student_age_eighteen():
    # TC-08: Студенту 18 лет в будни предоставляется скидка 25%
    assert calculate_ticket_price(18, "weekday", True) == 300.0


def test_student_weekend():
    # TC-09: Студент в выходной платит 375 рублей
    assert calculate_ticket_price(30, "weekend", True) == 375.0


def test_discounts_do_not_stack():
    # TC-10: До 18 лет применяется только детская скидка
    assert calculate_ticket_price(17, "weekday", True) == 200.0


def test_maximum_age():
    # TC-11: Возраст 120 лет допустим
    assert calculate_ticket_price(120, "weekend", False) == 500.0


def test_child_weekend():
    # TC-12: В 6 лет в выходной билет стоит 250 рублей
    assert calculate_ticket_price(6, "weekend", False) == 250.0


def test_negative_age():
    # TC-13: Отрицательный возраст — ошибка
    with pytest.raises(ValueError):
        calculate_ticket_price(-1, "weekday", False)


def test_age_above_maximum():
    # TC-14: Возраст больше 120 лет — ошибка
    with pytest.raises(ValueError):
        calculate_ticket_price(121, "weekend", False)


def test_invalid_day():
    # TC-15: Недопустимый день — ошибка
    with pytest.raises(ValueError):
        calculate_ticket_price(25, "holiday", False)


def test_invalid_student_type():
    # TC-16: Студенческий статус должен быть bool
    with pytest.raises(TypeError):
        calculate_ticket_price(25, "weekday", 1)


def test_fractional_age():
    # TC-17: Дробный возраст — ошибка типа
    with pytest.raises(TypeError):
        calculate_ticket_price(18.5, "weekday", False)


def test_empty_day():
    # TC-18: Пустое название дня — ошибка
    with pytest.raises(ValueError):
        calculate_ticket_price(25, "", False)
