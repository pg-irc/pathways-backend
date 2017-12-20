from django.core.validators import validate_slug
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import RequiredCharField

class TaxonomyTerm(models.Model):
    vocabulary = RequiredCharField(max_length=200, validators=[validate_slug])
    name = RequiredCharField(max_length=200, validators=[validate_slug])

    class Meta:
        verbose_name = _("taxonomy term")
        verbose_name_plural = _("taxonomy terms")
        unique_together = ('vocabulary', 'name')

    def __str__(self):
        return _("{name} in {vocabulary}").format(
            name=self.name, vocabulary=self.vocabulary
        )
