import urllib.parse
from rest_framework import test as rest_test
from rest_framework import status
from common.testhelpers.random_test_values import a_string
from push_notifications.models import PushNotificationToken


class CreatePushNotificationTokenTests(rest_test.APITestCase):
    def setUp(self):
        self.token = 'ExponentPushToken[_{}]'.format(a_string())
        self.url = urllib.parse.quote('/v1/push_notifications/tokens/{}/'.format(self.token))

    def test_put_creates_database_row(self):
        self.client.put(self.url, {'locale': 'en'})
        data = PushNotificationToken.objects.all()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].id, self.token)

    def test_put_returns_200(self):
        response = self.client.put(self.url, {'locale': 'en'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_returns_400_on_invalid_token(self):
        token = 'InvalidPushToken[{}]'.format(a_string())
        url = urllib.parse.quote('/v1/push_notifications/tokens/{}/'.format(token))
        response = self.client.put(url, {'locale': 'en'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_returns_400_on_invalid_locale(self):
        response = self.client.put(self.url, {'locale': 'this is way too long to be a valid locale'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_returns_resulting_data(self):
        response = self.client.put(self.url, {'locale': 'en'})

        self.assertEqual(response.json()['id'], self.token)
        self.assertEqual(response.json()['locale'], 'en')

    def test_put_returns_200_also_if_record_already_exists(self):
        PushNotificationToken(id=self.token, locale='en').save()
        response = self.client.put(self.url, {'locale': 'en'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_returns_updates_locale_if_record_already_exists(self):
        PushNotificationToken(id=self.token, locale='en').save()
        response = self.client.put(self.url, {'locale': 'fr'})
        self.assertEqual(response.json()['locale'], 'fr')

    def test_cannot_get_all(self):
        PushNotificationToken(id=self.token, locale='en').save()
        response = self.client.get('/v1/push_notifications/tokens/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_get_one(self):
        PushNotificationToken(id=self.token, locale='en').save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_post(self):
        response = self.client.post(self.url, {'locale': 'en'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
