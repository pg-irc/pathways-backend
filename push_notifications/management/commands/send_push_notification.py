from django.core.management.base import BaseCommand, CommandError
from push_notifications.models import PushNotificationToken

import csv


class Command(BaseCommand):
    help = ('')

    def add_arguments(self, parser):
        parser.add_argument('filename',
                            metavar='filename',
                            help='path to file containing text for notification, one locale per line')

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
    for token in PushNotificationToken.objects.all():
        pass
