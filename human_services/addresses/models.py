from django.db import models
from django.core import validators
from common.models import (ValidateOnSaveMixin, OptionalCharField,
                           OptionalTextField, RequiredCharField)


class Address(ValidateOnSaveMixin, models.Model):
    id = RequiredCharField(primary_key=True,
                        max_length=200,
                        validators=[validators.validate_slug])
    attention = OptionalCharField(max_length=200)
    address = OptionalTextField()
    city = RequiredCharField(max_length=200)
    state_province = OptionalCharField(max_length=200)
    postal_code = OptionalCharField(max_length=200)
    country = RequiredCharField(max_length=2)

    def __str__(self):
        return '{address}, {city} {state_province}, {country} {postal_code}'.format(
            address=self.address,
            city=self.city,
            state_province=self.state_province,
            postal_code=self.postal_code,
            country=self.country)

    class Meta:
        unique_together = ('attention', 'address', 'city',
                           'state_province', 'postal_code', 'country')

class AddressType(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
