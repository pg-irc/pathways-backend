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

    def test_post_can_create_a_token(self):
        the_token = a_string()
        body = {'id': the_token}
        url = '/v1/push_notifications/tokens/'
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json()), 1)
        data = PushNotificationToken.objects.all()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].id, the_token)
