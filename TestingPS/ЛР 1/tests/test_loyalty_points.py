import pytest
from loyalty_points import calculate_loyalty_points


class TestPositive:
    """Позитивные сценарии"""

    def test_tc01_economy_1_day(self):
        """TC-01: 1 день, economy, не постоянный."""
        assert calculate_loyalty_points(1, "economy", False) == 10

    def test_tc02_comfort_1_day(self):
        """TC-02: 1 день, comfort, не постоянный."""
        assert calculate_loyalty_points(1, "comfort", False) == 20

    def test_tc03_business_1_day(self):
        """TC-03: 1 день, business, не постоянный."""
        assert calculate_loyalty_points(1, "business", False) == 40

    def test_tc04_comfort_5_days_regular(self):
        """TC-04: 5 дней, comfort, постоянный."""
        assert calculate_loyalty_points(5, "comfort", True) == 165

    def test_tc05_business_10_days_regular(self):
        """TC-05: 10 дней, business, постоянный."""
        assert calculate_loyalty_points(10, "business", True) == 750

    def test_tc06_economy_60_days(self):
        """TC-06: 60 дней, economy, не постоянный."""
        assert calculate_loyalty_points(60, "economy", False) == 900


class TestNegative:
    """Негативные сценарии"""

    def test_tc07_zero_days(self):
        """TC-07: ноль дней → ValueError."""
        with pytest.raises(ValueError, match="rental_days"):
            calculate_loyalty_points(0, "economy", False)

    def test_tc08_negative_days(self):
        """TC-08: отрицательные дни → ValueError."""
        with pytest.raises(ValueError, match="rental_days"):
            calculate_loyalty_points(-5, "economy", False)

    def test_tc09_unknown_class(self):
        """TC-09: неизвестный класс → ValueError."""
        with pytest.raises(ValueError, match="car_class"):
            calculate_loyalty_points(3, "premium", False)

    def test_tc10_wrong_case_class(self):
        """TC-10: класс в другом регистре → ValueError."""
        with pytest.raises(ValueError, match="car_class"):
            calculate_loyalty_points(3, "Economy", False)


class TestBoundary:
    """Граничные значения"""

    def test_tc11_boundary_3_days(self):
        """TC-11: 3 дня — множитель ×1.0."""
        assert calculate_loyalty_points(3, "economy", False) == 30

    def test_tc12_boundary_4_days(self):
        """TC-12: 4 дня — множитель ×1.1."""
        assert calculate_loyalty_points(4, "economy", False) == 44

    def test_tc13_boundary_7_days(self):
        """TC-13: 7 дней — множитель ×1.1."""
        assert calculate_loyalty_points(7, "comfort", False) == 154

    def test_tc14_boundary_8_days(self):
        """TC-14: 8 дней — множитель ×1.25."""
        assert calculate_loyalty_points(8, "comfort", False) == 200

    def test_tc15_boundary_29_days(self):
        """TC-15: 29 дней — множитель ×1.25."""
        assert calculate_loyalty_points(29, "business", False) == 1450

    def test_tc16_boundary_30_days(self):
        """TC-16: 30 дней — множитель ×1.5."""
        assert calculate_loyalty_points(30, "business", False) == 1800


class TestEquivalenceClasses:
    """Проверка каждого класса эквивалентности"""

    def test_tc17_e1_days_le_zero(self):
        """TC-17 (E1): days ≤ 0 → ValueError."""
        with pytest.raises(ValueError):
            calculate_loyalty_points(-1, "economy", False)

    def test_tc18_e2_invalid_class(self):
        """TC-18 (E2): невалидный класс → ValueError."""
        with pytest.raises(ValueError):
            calculate_loyalty_points(3, "sport", False)

    def test_tc19_e3_short_rental(self):
        """TC-19 (E3): 1–3 дня, ×1.0."""
        assert calculate_loyalty_points(2, "economy", False) == 20

    def test_tc20_e4_week_rental(self):
        """TC-20 (E4): 4–7 дней, ×1.1."""
        assert calculate_loyalty_points(5, "economy", False) == 55

    def test_tc21_e5_middle_rental(self):
        """TC-21 (E5): 8–29 дней, ×1.25."""
        assert calculate_loyalty_points(15, "economy", False) == 188

    def test_tc22_e6_long_rental(self):
        """TC-22 (E6): ≥30 дней, ×1.5."""
        assert calculate_loyalty_points(30, "economy", False) == 450

    def test_tc23_e7_regular_customer(self):
        """TC-23 (E7): постоянный клиент, ×1.5."""
        assert calculate_loyalty_points(2, "economy", True) == 30

    def test_tc24_e8_regular_customer_false(self):
        """TC-24 (E8): обычный клиент, без множителя."""
        assert calculate_loyalty_points(2, "economy", False) == 20

    def test_tc25_e9_comfort_class(self):
        """TC-25 (E9): comfort-класс."""
        assert calculate_loyalty_points(1, "comfort", False) == 20


class TestAdditional:
    """Дополнительные сценарии"""

    def test_tc26_business_2_days_regular(self):
        """TC-26: 2 дня, business, постоянный."""
        assert calculate_loyalty_points(2, "business", True) == 120

    def test_tc27_rounding_half_to_even(self):
        """TC-27: 15 дней, comfort, постоянный → round(562.5) = 562."""
        assert calculate_loyalty_points(15, "comfort", True) == 562

    def test_tc28_business_45_days(self):
        """TC-28: 45 дней, business, не постоянный."""
        assert calculate_loyalty_points(45, "business", False) == 2700

    def test_tc29_business_1_day_regular(self):
        """TC-29: 1 день, business, постоянный (нижняя граница + флаг)."""
        assert calculate_loyalty_points(1, "business", True) == 60

    def test_tc30_economy_100_days_regular(self):
        """TC-30: 100 дней, economy, постоянный."""
        assert calculate_loyalty_points(100, "economy", True) == 2250
