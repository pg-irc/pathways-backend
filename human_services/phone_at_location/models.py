from django.db import models
from common.models import RequiredCharField
from human_services.locations.models import Location


class PhoneNumberType(models.Model):
    id = RequiredCharField(primary_key=True, max_length=200)


class PhoneAtLocation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='phone_numbers')
    phone_number_type = models.ForeignKey(PhoneNumberType, on_delete=models.PROTECT)
    phone_number = models.TextField()
