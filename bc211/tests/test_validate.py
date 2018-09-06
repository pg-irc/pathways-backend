import unittest
from common.testhelpers.random_test_values import a_string, a_list_of_integers, a_list_of_strings
from bc211 import validate, exceptions


class TestOptionalListOfObjects(unittest.TestCase):
    def test_throws_on_non_list_type_for_value(self):
        a_class = str
        a_field = a_string()
        a_value = a_string()
        with self.assertRaises(exceptions.InvalidTypeXmlParseException):
            validate.optional_list_of_objects(a_class, a_field, {a_field: a_value})

    def test_throws_on_wrong_type_for_list_item_value(self):
        a_class = str
        a_field = 'a_field'
        a_value = a_list_of_integers()
        with self.assertRaises(exceptions.InvalidTypeXmlParseException):
            validate.optional_list_of_objects(a_class, a_field, {a_field: a_value})

    def test_returns_expected_value_for_empty_list(self):
        a_class = str
        a_field = 'a_field'
        a_value = []
        self.assertEqual(validate.optional_list_of_objects(a_class, a_field, {a_field: a_value}), a_value)

    def test_returns_expected_value_for_list_of_specified_class(self):
        a_class = str
        a_field = 'a_field'
        a_value = a_list_of_strings()
        self.assertEqual(validate.optional_list_of_objects(a_class, a_field, {a_field: a_value}), a_value)
