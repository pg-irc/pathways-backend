import csv
import re
import logging
from django.core.management.base import BaseCommand, CommandError
from exponent_server_sdk import (DeviceNotRegisteredError, PushClient, PushMessage,
                                 PushResponseError, PushServerError)
from search.read_csv_data_from_file import read_csv_data_from_file

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = ('Send push notifications to a set of users identified by their expo push notification tokens')

    def add_arguments(self, parser):
        parser.add_argument('message',
                            metavar='message',
                            help=('path to file containing text for notification, '
                                  'comma separated, locale in first column, message in second column'))
        parser.add_argument('users',
                            metavar='users',
                            help=('path to file containing users, comma separated, expo push notification '
                                  'token in first column, locale in second column'))
        parser.add_argument('url',
                            metavar='url',
                            nargs='?',
                            help=('optional url to route to in the app, can be "store", "welcome" or "/task/<task id>"'),
                            default=None)

    def handle(self, *args, **options):
        users = options['users']
        users_csv = read_csv_data_from_file(users)
        valid_users = validate_users(users_csv)

        message = options['message']
        notifications = read_csv_data_from_file(message)
        valid_notifications = validate_localized_notifications(notifications)

        url = options['url']

        send_push_notifications(valid_users, valid_notifications, url)


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


def send_push_notifications(users, localized_notifications, url):
    for user in users:
        token = user['token']
        locale = user['locale']
        message = localized_notifications[locale]
        extra = build_extra_data(url)
        send_push_message(token, message, extra)


def build_extra_data(url):
    if url:
        return {'navigateToRoute': url}
    return None


def send_push_message(token, message, extra):
    try:
        response = PushClient().publish(PushMessage(to=token, body=message, data=extra))

    except PushServerError:
        LOGGER.error('Error pushing notification: PushServerError for %s', token)

    except (ConnectionError, HTTPError):
        LOGGER.error('Error pushing notification: ConnectionError for %s', token)

    try:
        response.validate_response()

    except DeviceNotRegisteredError:
        # According to https://github.com/expo/expo-server-sdk-python this error is
        # thrown when users no longer want to receive push notifications.
        LOGGER.warning('DeviceNotRegisteredError, remove this token from our database: %s', token)

    except PushResponseError:
        LOGGER.error('Error pushing notification: PushResponseError for %s', token)
