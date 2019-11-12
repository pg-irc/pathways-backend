from django.db import models
from common.models import RequiredCharField


class PushNotificationToken(models.Model):
    id = RequiredCharField(primary_key=True, max_length=200)
    locale = RequiredCharField(max_length=10)

    class Meta:
        ordering = ['id']
