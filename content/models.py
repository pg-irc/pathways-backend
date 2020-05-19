from common.models import ValidateOnSaveMixin, RequiredCharField
from django.core import validators
from django.db import models
from parler.models import TranslatableModel, TranslatedFields

class Alert(ValidateOnSaveMixin, TranslatableModel):
    id = RequiredCharField(primary_key=True,
                           max_length=200,
                           validators=[validators.validate_slug])

    translations = TranslatedFields(title=models.CharField(max_length=200),
                                    description=models.TextField(blank=True, null=True))

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title
