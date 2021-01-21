import uuid
from django.core.validators import validate_slug
from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import RequiredCharField


# TODO remove
def default_term_id():
    return str(uuid.uuid4())


class TaxonomyTerm(models.Model):
    id = RequiredCharField(primary_key=True, default=default_term_id, max_length=200,
                                         validators=[validate_slug])
    taxonomy_id = RequiredCharField(max_length=200, validators=[validate_slug])
    name = RequiredCharField(max_length=200, validators=[validate_slug])

    class Meta:
        verbose_name = _('taxonomy term')
        verbose_name_plural = _('taxonomy terms')
        unique_together = ('taxonomy_id', 'name')

    def __str__(self):
        return '{name} in {taxonomy_id}'.format(
            name=self.name, taxonomy_id=self.taxonomy_id
        )
