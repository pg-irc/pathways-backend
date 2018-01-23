from django.db import models
from django.core.exceptions import ValidationError

from common.models import ValidateOnSaveMixin, OptionalCharField, RequiredCharField


class Address(ValidateOnSaveMixin, models.Model):
    attention = OptionalCharField(max_length=200)
    address = models.TextField()
    city = RequiredCharField(max_length=200)
    state_province = OptionalCharField(max_length=200)
    postal_code = OptionalCharField(max_length=200)
    country = RequiredCharField(max_length=2)

    class Meta:
        unique_together = ('attention', 'address', 'city', 'state_province', 'postal_code', 'country')

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except ValidationError:
            return

class AddressType(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
