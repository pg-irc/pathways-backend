from django.db import models
from django.core.exceptions import ValidationError

from common.models import ValidateOnSaveMixin


class Address(ValidateOnSaveMixin, models.Model):
    attention = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=200)
    state_province = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=2)

    class Meta:
        unique_together = ('address', 'city')

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except ValidationError:
            return

class AddressType(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
