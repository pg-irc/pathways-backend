from django.test import TestCase
from django.core.management.base import CommandError
from push_notifications.management.commands.send_push_notification import validate_localized_notifications, validate_user


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
            validate_localized_notifications(data)

class ValidateUsersTests(TestCase):
    def test_returns_user_with_token(self):
        user = validate_user(['ExponentPushToken[foo]', 'en'])
        self.assertEqual(user['token'], 'ExponentPushToken[foo]')

    def test_returns_user_with_locale(self):
        user = validate_user(['ExponentPushToken[foo]', 'en'])
        self.assertEqual(user['locale'], 'en')

    def test_throws_on_invalid_token_format(self):
        with self.assertRaisesMessage(CommandError, 'BadToken[foo]: Invalid token'):
            validate_user(['BadToken[foo]', 'en'])

    def test_throws_on_invalid_locale(self):
        with self.assertRaisesMessage(CommandError, 'xy: Invalid locale'):
            validate_user(['ExponentPushToken[foo]', 'xy'])
