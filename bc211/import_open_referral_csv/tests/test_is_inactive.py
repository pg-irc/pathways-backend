from django.test import TestCase
from common.testhelpers.random_test_values import an_integer
from bc211.is_inactive import is_inactive

# pylint: disable=invalid-name
class IsInactiveTests(TestCase):
    def test_detects_inactive_record_when_DEL_is_uppercase(self):
        description = 'DEL' + str(an_integer(min=10, max=99))
        self.assertTrue(is_inactive(description))

    def test_detects_inactive_record_when_DEL_is_lowercase_characters(self):
        description = 'Del' + str(an_integer(min=10, max=99))
        self.assertTrue(is_inactive(description))

    def test_detects_inactive_record_when_DEL_has_space_after(self):
        description = 'DEL ' + str(an_integer(min=10, max=99))
        self.assertTrue(is_inactive(description))

    def test_returns_false_when_description_is_not_marked_inactive(self):
        description = 'Delivers settlement services'
        self.assertFalse(is_inactive(description))
