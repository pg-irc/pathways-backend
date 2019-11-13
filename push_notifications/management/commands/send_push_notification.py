import csv
import re
from django.core.management.base import BaseCommand, CommandError
from exponent_server_sdk import (DeviceNotRegisteredError, PushClient, PushMessage, 
                                 PushResponseError, PushServerError)



class Command(BaseCommand):
    help = ('')

    def add_arguments(self, parser):
        parser.add_argument('message',
                            metavar='message',
                            help=('path to file containing text for notification, '
                                'comma separated, locale in first column, message in second column'))
        parser.add_argument('users',
                            metavar='users',
                            help=(''))

    def handle(self, *args, **options):
        users = options['users']
        users_csv = read_csv_data_from_file(users)
        valid_users = validate_users(users_csv)

        message = options['message']
        notifications = read_csv_data_from_file(message)
        valid_notifications = validate_localized_notifications(notifications)

        send_push_notifications(valid_users, valid_notifications)


# TODO move this to a common spot
def read_csv_data_from_file(csv_path):
    result = []
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            result.append(row)
    return result

def validate_users(users):
    result = []
    for line in users:
        result.append(validate_user(line))
    return result

def validate_user(user):
    locale = validate_locale(user[1])
    token = validate_token(user[0])
    return {'token': token, 'locale': locale}

def validate_locale(locale):
    if not locale in ['ar', 'en', 'fr', 'ko', 'pa', 'tl', 'zh_CN', 'zh_TW']:
        raise CommandError('{}: Invalid locale'.format(locale))
    return locale

def validate_token(token):
    match = re.search(r'^ExponentPushToken\[.*\]$', token)
    if not match:
        raise CommandError('{}: Invalid token'.format(token))
    return token

def validate_localized_notifications(notifications):
    result = {}
    for line in notifications:
        locale = validate_locale(line[0])
        result[locale] = line[1]
    return result

def send_push_notifications(users, localized_notifications):
    for user in users:
        token = user['token']
        locale = user['locale']
        message = localized_notifications[locale]
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
