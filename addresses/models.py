from django.db import models

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

class AddressType(models.Model):
    type = models.CharField(max_length=200)
