from common.models import ValidateOnSaveMixin, RequiredCharField
from django.core import validators
from django.db import models
from django.utils.functional import cached_property
from organizations.models import Organization
from parler.models import TranslatableModel, TranslatedFields

class Service(ValidateOnSaveMixin, TranslatableModel):
    id = RequiredCharField(primary_key=True, max_length=200, validators=[validators.validate_slug])
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='services')
    translations = TranslatedFields(
        name=models.CharField(max_length=200),
        description=models.TextField(blank=True, null=True),
        location_description=models.TextField(blank=True, null=True)
    )

    def __str__(self):
        return self.name
