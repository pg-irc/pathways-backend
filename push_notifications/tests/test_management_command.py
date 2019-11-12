from django.test import TestCase
from django.core.management.base import CommandError
from push_notifications.management.commands.send_push_notification import validate_localized_notifications


class ValidateNotificationsTests(TestCase):
    def test_returns_map_with_message(self):
        data = [['en', 'message']]
        valid_data = validate_localized_notifications(data)
        self.assertEqual(valid_data['en'], 'message')

    def test_returns_map_with_two_localized_message(self):
        data = [['en', 'message'], ['fr', 'fr_message']]
        valid_data = validate_localized_notifications(data)
        self.assertEqual(valid_data['en'], 'message')
        self.assertEqual(valid_data['fr'], 'fr_message')

    def test_throws_error_on_invalid_locale_code(self):
        data = [['xy', 'message']]
        with self.assertRaisesMessage(CommandError, 'xy: Invalid locale'):
            valid_data = validate_localized_notifications(data)
