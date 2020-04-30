import re
from django.core.exceptions import ValidationError
from django.conf import settings


def validate_token(value):
    if not re.match(r'^ExponentPushToken\[.*\]$', value):
        raise ValidationError('{}: Invalid token'.format(value))


def validate_api_key(value):
    if value != settings.PATHWAYS_API_KEY:
        raise ValidationError('Invalid API key')
