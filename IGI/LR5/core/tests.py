from django.test import TestCase
from django.core.exceptions import ValidationError

from core.validators import validate_phone_by_format_375_29


class ValidatorsTest(TestCase):
    """Тесты для валидаторов"""

    def test_valid_phone_375_29(self):
        # Should not raise
        validate_phone_by_format_375_29("+375 (29) 111-11-11")
        validate_phone_by_format_375_29("+37529111111")

    def test_invalid_phone_wrong_prefix(self):
        with self.assertRaises(ValidationError):
            validate_phone_by_format_375_29("+375 (28) 111-11-11")

    def test_invalid_phone_empty(self):
        with self.assertRaises(ValidationError):
            validate_phone_by_format_375_29("")

    def test_invalid_phone_without_country_code(self):
        with self.assertRaises(ValidationError):
            validate_phone_by_format_375_29("(29) 111-11-11")
