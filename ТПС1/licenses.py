# licenses.py

def calculate_license_cost(license_type: str, seats_count: int, is_annual: bool) -> float:
    """
    Расчёт стоимости лицензии.

    Бизнес-правила:
    1. Если seats_count < 1 - ValueError.
    2. Если license_type не равен 'trial', 'standard' или 'team' - ValueError.
    3. Если license_type == 'trial': (бесплатная пробная лицензия)
       - seats_count == 1: 0.0 
       - иначе: ValueError (только для 1 человека)
    4. Если license_type == 'standard': (стандартная лицензия)
       - seats_count == 1: 500.0
       - иначе: ValueError (только для 1 человека)
    5. Если license_type == 'team': (командная лицензия - 600.0 за человека)
       - 2 <= seats_count <= 100: seats_count * 600.0
       - иначе: ValueError (только от 2 до 100 человек)
    6. Для is_annual=True применяется скидка 10% на итоговую стоимость.
    """
    if seats_count < 1:
        raise ValueError("seats_count must be >= 1")
    if license_type not in ('trial', 'standard', 'team'):
        raise ValueError("license_type must be 'trial', 'standard' or 'team'")

    if license_type == 'trial':
        if seats_count == 1:
            cost = 0.0
        else:
            raise ValueError("trial license is only for 1 seat")

    elif license_type == 'standard':
        if seats_count == 1:
            cost = 500.0
        else:
            raise ValueError("standard license is only for 1 seat")

    else:  # team
        if 2 <= seats_count <= 100:
            cost = seats_count * 600.0
        else:
            raise ValueError("team license requires 2 to 100 seats")

    if is_annual:
        cost *= 0.9

    return cost