from django.db import models
from common.models import RequiredCharField
from push_notifications.validation import validate_token
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_api_key(value):
    if PathwaysApiKey.objects.filter(pk=value).exists():
        return
    if value != settings.PATHWAYS_API_KEY:
        raise ValidationError('Invalid API key')


class PathwaysApiKey(models.Model):
    id = RequiredCharField(primary_key=True, max_length=200)


class PushNotificationToken(models.Model):
    id = RequiredCharField(primary_key=True, max_length=200, validators=[validate_token])
    locale = RequiredCharField(max_length=10)
    updated_at = models.DateTimeField(auto_now=True)
    api_key = RequiredCharField(max_length=50, validators=[validate_api_key])

    def clean(self):
        self.api_key = 'omitted_from_database'
        super(PushNotificationToken, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(PushNotificationToken, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']
