from common.testhelpers.random_test_values import a_string
from push_notifications.models import PushNotificationToken


def create_push_notification_token():
    result = PushNotificationToken()
    result.id = a_string()
    result.save()
    return result
