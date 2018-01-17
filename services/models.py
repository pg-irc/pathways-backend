from common.models import ValidateOnSaveMixin, RequiredCharField
from django.core import validators
from django.db import models
from organizations.models import Organization
from parler.models import TranslatableModel, TranslatedFields
from taxonomies.models import TaxonomyTerm

class Service(ValidateOnSaveMixin, TranslatableModel):
    id = RequiredCharField(primary_key=True,
                           max_length=200,
                           validators=[validators.validate_slug])

    organization = models.ForeignKey(Organization,
                                     on_delete=models.CASCADE,
                                     related_name='services')

    taxonomy_terms = models.ManyToManyField(TaxonomyTerm,
                                            db_table='services_service_taxonomy_terms')

    translations = TranslatedFields(name=models.CharField(max_length=200),
                                    description=models.TextField(blank=True, null=True))

    def __str__(self):
        return self.name
