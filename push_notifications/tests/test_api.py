from rest_framework import test as rest_test
from rest_framework import status
from common.testhelpers.random_test_values import a_string
from push_notifications.models import PushNotificationToken
from push_notifications.tests.helpers import create_push_notification_token


class CreatePushNotificationTokenTests(rest_test.APITestCase):
    def setUp(self):
        self.token = a_string()
        self.url = '/hello/{}/'.format(self.token)

    def test_put_creates_database_row(self):
        self.client.put(self.url, {'locale': 'en'})
        data = PushNotificationToken.objects.all()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].id, self.token)

    def test_put_returns_200(self):
        response = self.client.put(self.url, {'locale': 'en'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_returns_400_on_invalid_locale(self):
        response = self.client.put(self.url, {'locale': 'this is way too long to be a valid locale'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_returns_resulting_data(self):
        response = self.client.put(self.url, {'locale': 'en'})
        content = str(response.content, encoding='utf8')

        self.assertJSONEqual(content, {'id': self.token, 'locale': 'en'})

    def test_put_returns_200_also_if_record_already_exists(self):
        PushNotificationToken(id=self.token, locale='en').save()
        response = self.client.put(self.url, {'locale': 'en'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_returns_updates_locale_if_record_already_exists(self):
        PushNotificationToken(id=self.token, locale='en').save()
        response = self.client.put(self.url, {'locale': 'fr'})
        content = str(response.content, encoding='utf8')
        self.assertJSONEqual(content, {'id': self.token, 'locale': 'fr'})
