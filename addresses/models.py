from django.db import models
from common.models import ValidateOnSaveMixin, OptionalCharField, RequiredCharField


class Address(ValidateOnSaveMixin, models.Model):
    address = models.TextField()
    city = RequiredCharField(max_length=200)
    country = RequiredCharField(max_length=2)
    attention = OptionalCharField(max_length=200)
    state_province = OptionalCharField(max_length=200)
    postal_code = OptionalCharField(max_length=200)

    class Meta:
        unique_together = ('address', 'city', 'country',
                           'attention', 'state_province', 'postal_code')

class AddressType(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
