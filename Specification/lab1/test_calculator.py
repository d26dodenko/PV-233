import unittest

from calculator import (
    add, subtract, multiply, divide, power, calculate, classify_number,
)


class TestBasicOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(multiply(4, 3), 12)

    def test_divide(self):
        self.assertEqual(divide(10, 4), 2.5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(1, 0)

    def test_power(self):
        self.assertEqual(power(2, 10), 1024)


class TestCalculate(unittest.TestCase):
    def test_all_operations(self):
        cases = [
            (2, "+", 3, 5),
            (5, "-", 3, 2),
            (4, "*", 3, 12),
            (10, "/", 4, 2.5),
            (2, "**", 3, 8),
        ]
        for a, op, b, expected in cases:
            with self.subTest(op=op):
                self.assertEqual(calculate(a, op, b), expected)

    def test_unknown_operation(self):
        with self.assertRaises(ValueError):
            calculate(1, "%", 2)


class TestClassifyNumber(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(classify_number(5), "Positive")

    def test_zero(self):
        self.assertEqual(classify_number(0), "Zero")

    def test_negative(self):
        self.assertEqual(classify_number(-5), "Negative")


if __name__ == "__main__":
    unittest.main()
