from rest_framework import test as rest_test
from rest_framework import status
from common.testhelpers.random_test_values import a_string
from push_notifications.models import PushNotificationToken


def create_push_notification_token():
    result = PushNotificationToken()
    result.id = a_string()
    result.save()
    return result


class ServicesApiTests(rest_test.APITestCase):

    def test_can_get_tokens(self):
        create_push_notification_token()
        create_push_notification_token()
        url = '/v1/push_notifications/tokens/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
