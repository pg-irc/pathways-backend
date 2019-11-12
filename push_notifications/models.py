from django.db import models
from django.core import validators
from common.models import RequiredCharField


class PushNotificationToken(models.Model):
    id = RequiredCharField(primary_key=True, max_length=200)

    class Meta:
        ordering = ['id']
