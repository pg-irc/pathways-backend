import re
from django.core.exceptions import ValidationError


def validate_token(value):
    if not re.match(r'^ExponentPushToken\[.*\]$', value):
        raise ValidationError('{}: Invalid token'.format(value))
