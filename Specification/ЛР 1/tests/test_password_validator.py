import unittest
from password_validator import validate_password, strength

class TestPasswordValidator(unittest.TestCase):

    def test_valid_password(self):
        result = validate_password("Abcdef1!")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_too_short(self):
        result = validate_password("Ab1!")
        self.assertIn("too_short", result["errors"])

    def test_no_uppercase(self):
        self.assertIn("no_uppercase", validate_password("abcdef1!")["errors"])

    def test_no_digit(self):
        self.assertIn("no_digit", validate_password("Abcdefg!")["errors"])

    def test_no_special(self):
        self.assertIn("no_special", validate_password("Abcdefg1")["errors"])

    def test_strength_weak(self):
        self.assertEqual(strength("abc"), "weak")

    def test_strength_medium(self):
        self.assertEqual(strength("Abcdefg1"), "medium")

    def test_strength_strong(self):
        self.assertEqual(strength("Abcdefg1!"), "strong")

    def test_no_lowercase(self):
        self.assertIn("no_lowercase", validate_password("ABCDEF1!")["errors"])

if __name__ == "__main__":
    unittest.main()
