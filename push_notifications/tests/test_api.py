from rest_framework import test as rest_test
from rest_framework import status
from common.testhelpers.random_test_values import a_string
from push_notifications.models import PushNotificationToken
from push_notifications.tests.helpers import create_push_notification_token


class HelloTests(rest_test.APITestCase):
    def test_foo(self):
        response = self.client.get('/hello/')
        self.assertEqual(response.json()['message'], 'Hello, world!')


class ServicesApiTests(rest_test.APITestCase):
    def setUp(self):
        self.url = '/v1/push_notifications/tokens/'

    def test_can_get_token(self):
        token = create_push_notification_token()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['id'], token.id)

    def test_can_get_tokens(self):
        create_push_notification_token()
        create_push_notification_token()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_post_creates_new_database_row(self):
        the_token = a_string()
        self.client.post(self.url, {'id': the_token, 'locale': 'en'})
        data = PushNotificationToken.objects.all()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].id, the_token)

    def test_post_returns_201_on_success(self):
        response = self.client.post(self.url, {'id': a_string(), 'locale': 'en'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_returns_data_on_success(self):
        the_token = a_string()
        response = self.client.post(self.url, {'id': the_token, 'locale': 'en'})
        self.assertEqual(response.json()['id'], the_token)
        self.assertEqual(response.json()['locale'], 'en')

    def test_post_returns_400_on_record_already_exists(self):
        record = create_push_notification_token()
        response = self.client.post(self.url, {'id': record.id, 'locale': 'en'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['id'][0].code, 'unique')
