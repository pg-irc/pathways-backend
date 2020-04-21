from django.db import models
from common.models import RequiredCharField
from push_notifications.validation import validate_token, validate_api_key


class PushNotificationToken(models.Model):
    id = RequiredCharField(primary_key=True, max_length=200, validators=[validate_token])
    locale = RequiredCharField(max_length=10)
    updated_at = models.DateTimeField(auto_now=True)
    api_key = RequiredCharField(max_length=50, validators=[validate_api_key])

    def clean(self):
        # there is no need to store the API key in the database
        self.api_key = 'blabla'
        super(PushNotificationToken, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(PushNotificationToken, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']
