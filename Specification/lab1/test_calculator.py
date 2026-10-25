import sys
import unittest
from unittest.mock import patch
from io import StringIO

# Импортируем функцию main из нашего скрипта calculator.py
from calculator import main

class TestCalculator(unittest.TestCase):

    def run_calculator(self, args):
        """Вспомогательный метод для перехвата stdout и вызова main с аргументами."""
        with patch.object(sys, 'argv', ['calculator.py'] + args):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                try:
                    main()
                    exit_code = 0
                except SystemExit as e:
                    exit_code = e.code
                return fake_out.getvalue().strip(), exit_code

    # --- Успешные сценарии (Арифметика) ---

    def test_addition(self):
        output, code = self.run_calculator(['5', '+', '3'])
        self.assertEqual(code, 0)
        self.assertEqual(output, '8')

    def test_subtraction(self):
        output, code = self.run_calculator(['10', '-', '4'])
        self.assertEqual(code, 0)
        self.assertEqual(output, '6')

    def test_multiplication(self):
        output, code = self.run_calculator(['2.5', '*', '4'])
        self.assertEqual(code, 0)
        self.assertEqual(output, '10')

    def test_division_float_result(self):
        output, code = self.run_calculator(['7', '/', '2'])
        self.assertEqual(code, 0)
        self.assertEqual(output, '3.5')

    # --- Сценарии обработки ошибок ---

    def test_invalid_arg_count(self):
        output, code = self.run_calculator(['5', '+'])
        self.assertEqual(code, 1)
        self.assertIn("Usage:", output)

    def test_invalid_number_conversion(self):
        output, code = self.run_calculator(['abc', '+', '5'])
        self.assertEqual(code, 1)
        self.assertEqual(output, "Error: Invalid number")

    def test_division_by_zero(self):
        output, code = self.run_calculator(['10', '/', '0'])
        self.assertEqual(code, 1)
        self.assertEqual(output, "Error: Division by zero")

    def test_unknown_operator(self):
        output, code = self.run_calculator(['5', '^', '2'])
        self.assertEqual(code, 1)
        self.assertEqual(output, "Error: Unknown operator")


if __name__ == '__main__':
    unittest.main()