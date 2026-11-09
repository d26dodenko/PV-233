"""Расчёт стоимости билета в кино."""


def calculate_ticket_price(age: int, day: str, is_student: bool) -> float:
    """Рассчитать стоимость билета по возрасту, дню и студенческому статусу.

    Будни: 400 руб., выходные: 500 руб.
    Дети младше 6 лет проходят бесплатно.
    С 6 до 17 лет включительно — скидка 50%.
    С 18 лет при студенческом статусе — скидка 25%.
    Скидки не суммируются.
    """
    if type(age) is not int:
        raise TypeError("age must be an integer")
    if age < 0 or age > 120:
        raise ValueError("age must be between 0 and 120")
    if day not in ("weekday", "weekend"):
        raise ValueError("day must be weekday or weekend")
    if type(is_student) is not bool:
        raise TypeError("is_student must be bool")

    if age < 6:
        return 0.0

    price = 400.0 if day == "weekday" else 500.0
    if age < 18:
        price *= 0.5
    elif is_student:
        price *= 0.75

    return price
