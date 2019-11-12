import csv
from django.core.management.base import BaseCommand, CommandError
from exponent_server_sdk import (DeviceNotRegisteredError, PushClient, PushMessage, 
                                 PushResponseError, PushServerError)



class Command(BaseCommand):
    help = ('')

    def add_arguments(self, parser):
        parser.add_argument('filename',
                            metavar='filename',
                            help=('path to file containing text for notification, '
                                'comma separated, locale in first column, message in second column'))

    def handle(self, *args, **options):
        filename = options['filename']
        notifications = read_csv_data_from_file(filename)
        valid_notifications = validate_localized_notifications(notifications)
        send_push_notifications(valid_notifications)


# TODO move this to a common spot
def read_csv_data_from_file(csv_path):
    result = []
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            result.append(row)
    return result


def validate_localized_notifications(notifications):
    result = {}
    for line in notifications:
        locale = validate_locale(line[0])
        result[locale] = line[1]
    return result


class InvalidPushNotification(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def validate_locale(locale):
    if not locale in ['ar', 'en', 'fr', 'ko', 'pa', 'tl', 'zh_CN', 'zh_TW']:
        raise CommandError('{}: Invalid locale in push notification data'.format(locale))
    return locale


def send_push_notifications(notifications):
    for row in PushNotificationToken.objects.all():
        token = row.id
        message = notifications[row.locale]
        send_push_message(token, message)

def send_push_message(token, message, extra=None):
    try:
        response = PushClient().publish(PushMessage(to=token, body=message, data=extra))
    except PushServerError:
        print('Error pushing notification: PushServerError')
        raise
    except (ConnectionError, HTTPError):
        print('Error pushing notification: ConnectionError')
        raise

    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        print('Error pushing notification: DeviceNotRegisteredError')
    except PushResponseError:
        print('Error pushing notification: PushResponseError')
