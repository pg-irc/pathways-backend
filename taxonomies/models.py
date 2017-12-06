from django.core.validators import validate_slug
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from common.models import RequiredCharField


class Taxonomy(models.Model):
    vocabulary = RequiredCharField(max_length=200, validators=[validate_slug])
    name = RequiredCharField(max_length=200, validators=[validate_slug])

    class Meta:
        verbose_name = "vocabulary"
        verbose_name_plural = "taxonomies"
        unique_together = ('vocabulary', 'name')

    def __str__(self):
        return _("{name} in {vocabulary}").format(
            name=self.name, vocabulary=self.vocabulary
        )

    def save(self, *args, **kwargs):
        self.vocabulary = slugify(self.vocabulary)
        self.name = slugify(self.name)
        return super(Taxonomy, self).save(*args, **kwargs)
