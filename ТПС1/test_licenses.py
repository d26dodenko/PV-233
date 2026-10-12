import pytest
from licenses import calculate_license_cost


def test_trial_license():
    # TC-01: Бесплатная пробная лицензия на 1 человека - бесплатно
    assert calculate_license_cost('trial', 1, False) == 0.0


def test_standard_license():
    # TC-02: Стандартная лицензия на 1 человека - 500
    assert calculate_license_cost('standard', 1, False) == 500.0


def test_team_license():
    # TC-03: Командная лицензия на 2 человек - 1200
    assert calculate_license_cost('team', 2, False) == 1200.0


def test_team_license_max_seats():
    # TC-04: Командная лицензия на 100 человек - 60000
    assert calculate_license_cost('team', 100, False) == 60000.0


def test_trial_license_annual():
    # TC-05: Годовая пробная лицензия остаётся бесплатной
    assert calculate_license_cost('trial', 1, True) == 0.0


def test_standard_license_annual():
    # TC-06: Годовая стандартная лицензия со скидкой 10%
    assert calculate_license_cost('standard', 1, True) == 450.0


def test_team_license_annual():
    # TC-07: Годовая командная лицензия со скидкой 10%
    assert calculate_license_cost('team', 2, True) == 1080.0


def test_negative_seats():
    # TC-08: Отрицательное количество мест - ошибка
    with pytest.raises(ValueError):
        calculate_license_cost('team', -1, False)


def test_zero_seats():
    # TC-09: Ноль мест - ошибка
    with pytest.raises(ValueError):
        calculate_license_cost('team', 0, False)


def test_invalid_license_type():
    # TC-10: Неизвестный тип лицензии - ошибка
    with pytest.raises(ValueError):
        calculate_license_cost('premium', 1, False)


def test_trial_license_multiple_seats():
    # TC-11: Бесплатная пробная лицензия доступна только для 1 человека
    with pytest.raises(ValueError):
        calculate_license_cost('trial', 2, False)


def test_standard_license_multiple_seats():
    # TC-12: Стандартная лицензия доступна только для 1 человека
    with pytest.raises(ValueError):
        calculate_license_cost('standard', 2, False)


def test_team_license_one_seat():
    # TC-13: Командная лицензия рассчитана минимум на 2 человек
    with pytest.raises(ValueError):
        calculate_license_cost('team', 1, False)


def test_team_license_more_than_100_seats():
    # TC-14: Командная лицензия рассчитана максимум на 100 человек
    with pytest.raises(ValueError):
        calculate_license_cost('team', 101, False)