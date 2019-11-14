from django.db import models
from common.models import RequiredCharField
from push_notifications.validation import validate_token


class PushNotificationToken(models.Model):
    id = RequiredCharField(primary_key=True, max_length=200, validators=[validate_token])
    locale = RequiredCharField(max_length=10)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
