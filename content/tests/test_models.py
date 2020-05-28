from django.test import TestCase
from django.core import exceptions
from content.tests.helpers import AlertBuilder
from common.testhelpers.random_test_values import a_string
from common.testhelpers.database import validate_save_and_reload


# pylint: disable=too-many-public-methods
class TestAlertModel(TestCase):
    def test_has_id_field(self):
        alert_id = a_string()
        alert = AlertBuilder().with_id(alert_id).build()
        alert_from_db = validate_save_and_reload(alert)
        self.assertEqual(alert_from_db.id, alert_id)

    def test_id_cannot_be_none(self):
        alert_id = None
        alert = AlertBuilder().with_id(alert_id).build()
        with self.assertRaises(exceptions.ValidationError):
            alert.full_clean()

    def test_id_cannot_be_empty(self):
        alert_id = ''
        alert = AlertBuilder().with_id(alert_id).build()
        with self.assertRaises(exceptions.ValidationError):
            alert.full_clean()

    def test_has_heading_field(self):
        heading = a_string()
        alert = AlertBuilder().with_heading(heading).build()
        alert_from_db = validate_save_and_reload(alert)
        self.assertEqual(alert_from_db.heading, heading)

    def test_title_is_multilingual(self):
        alert = AlertBuilder().build()
        set_heading_in_language(alert, 'en', 'In English')
        set_heading_in_language(alert, 'fr', 'En français')
        alert_from_db = validate_save_and_reload(alert)

        self.assert_title_in_language_equals(alert_from_db, 'en', 'In English')
        self.assert_title_in_language_equals(alert_from_db, 'fr', 'En français')

    def assert_title_in_language_equals(self, alert, language, expected_text):
        alert.set_current_language(language)
        self.assertEqual(alert.heading, expected_text)

    def test_has_content_field(self):
        content = a_string()
        alert = AlertBuilder().with_content(content).build()
        alert_from_db = validate_save_and_reload(alert)
        self.assertEqual(alert_from_db.content, content)

    def test_description_is_multilingual(self):
        alert = AlertBuilder().build()
        set_content_in_language(alert, 'en', 'In English')
        set_content_in_language(alert, 'fr', 'En français')
        alert_from_db = validate_save_and_reload(alert)

        self.assert_description_in_language_equals(alert_from_db, 'en', 'In English')
        self.assert_description_in_language_equals(alert_from_db, 'fr', 'En français')

    def assert_description_in_language_equals(self, alert, language, expected_text):
        alert.set_current_language(language)
        self.assertEqual(alert.content, expected_text)


def set_heading_in_language(alert, language, text):
    alert.set_current_language(language)
    alert.heading = text


def set_content_in_language(alert, language, text):
    alert.set_current_language(language)
    alert.content = text
